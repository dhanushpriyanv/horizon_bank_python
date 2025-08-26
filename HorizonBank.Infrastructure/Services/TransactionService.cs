using AutoMapper;
using HorizonBank.Core.DTOs;
using HorizonBank.Core.Entities;
using HorizonBank.Core.Exceptions;
using HorizonBank.Core.Interfaces;

namespace HorizonBank.Infrastructure.Services;

public class TransactionService : ITransactionService
{
    private readonly ITransactionRepository _transactionRepository;
    private readonly IAccountRepository _accountRepository;
    private readonly ICustomerRepository _customerRepository;
    private readonly IMapper _mapper;

    public TransactionService(
        ITransactionRepository transactionRepository,
        IAccountRepository accountRepository,
        ICustomerRepository customerRepository,
        IMapper mapper)
    {
        _transactionRepository = transactionRepository;
        _accountRepository = accountRepository;
        _customerRepository = customerRepository;
        _mapper = mapper;
    }

    public async Task<IEnumerable<TransactionDto>> GetAllTransactionsAsync()
    {
        var transactions = await _transactionRepository.GetAllAsync();
        return _mapper.Map<IEnumerable<TransactionDto>>(transactions);
    }

    public async Task<TransactionDto?> GetTransactionByIdAsync(int id)
    {
        var transaction = await _transactionRepository.GetByIdAsync(id);
        return transaction != null ? _mapper.Map<TransactionDto>(transaction) : null;
    }

    public async Task<IEnumerable<TransactionDto>> GetTransactionsByCustomerIdAsync(int customerId)
    {
        var transactions = await _transactionRepository.GetByCustomerIdAsync(customerId);
        return _mapper.Map<IEnumerable<TransactionDto>>(transactions);
    }

    public async Task<TransactionDto> TransferMoneyAsync(TransferMoneyDto transferDto)
    {
        var senderAccount = await _accountRepository.GetByCustomerIdAsync(transferDto.FromCustomerId);
        var receiverAccount = await _accountRepository.GetByCustomerIdAsync(transferDto.ToCustomerId);

        if (senderAccount == null)
            throw new AccountNotFoundException("Sender account not found");
        if (receiverAccount == null)
            throw new AccountNotFoundException("Receiver account not found");
        if (senderAccount.Balance < transferDto.Amount)
            throw new InsufficientFundsException("Insufficient funds");

        // Update balances
        senderAccount.Balance -= transferDto.Amount;
        receiverAccount.Balance += transferDto.Amount;

        await _accountRepository.UpdateAsync(senderAccount);
        await _accountRepository.UpdateAsync(receiverAccount);

        // Create debit transaction
        var debitTransaction = new Transaction
        {
            AccountId = senderAccount.Id,
            FromCustomer = senderAccount.CustomerId,
            ToCustomer = receiverAccount.CustomerId,
            Amount = -Math.Abs(transferDto.Amount),
            Type = "DEBIT",
            Timestamp = DateTime.UtcNow
        };

        var createdDebitTransaction = await _transactionRepository.CreateAsync(debitTransaction);

        // Create credit transaction
        var creditTransaction = new Transaction
        {
            AccountId = receiverAccount.Id,
            FromCustomer = senderAccount.CustomerId,
            ToCustomer = receiverAccount.CustomerId,
            Amount = Math.Abs(transferDto.Amount),
            Type = "CREDIT",
            Timestamp = DateTime.UtcNow
        };

        await _transactionRepository.CreateAsync(creditTransaction);

        return _mapper.Map<TransactionDto>(createdDebitTransaction);
    }

    public async Task<TransactionDto> PayBillAsync(BillPayDto billPayDto)
    {
        var customer = await _customerRepository.GetByIdAsync(billPayDto.CustomerId);
        if (customer == null)
            throw new CustomerNotFoundException("Customer not found");

        var account = await _accountRepository.GetByCustomerIdAsync(billPayDto.CustomerId);
        if (account == null)
            throw new AccountNotFoundException("Account not found");

        if (account.Balance < billPayDto.Amount)
            throw new InsufficientFundsException("Insufficient funds");

        account.Balance -= billPayDto.Amount;
        await _accountRepository.UpdateAsync(account);

        var transaction = new Transaction
        {
            FromCustomer = customer.Id,
            ToCustomer = customer.Id,
            Amount = -Math.Abs(billPayDto.Amount),
            Timestamp = DateTime.UtcNow,
            AccountId = account.Id,
            Type = $"BILL_PAY_{billPayDto.BillType.ToUpper()}"
        };

        var createdTransaction = await _transactionRepository.CreateAsync(transaction);
        return _mapper.Map<TransactionDto>(createdTransaction);
    }

    public async Task<TransactionDto> AddMoneyAsync(AddMoneyDto addMoneyDto)
    {
        var customer = await _customerRepository.GetByIdAsync(addMoneyDto.CustomerId);
        if (customer == null)
            throw new CustomerNotFoundException("Customer not found");

        var account = await _accountRepository.GetByCustomerIdAsync(addMoneyDto.CustomerId);
        if (account == null)
            throw new AccountNotFoundException("Account not found");

        account.Balance += addMoneyDto.Amount;
        await _accountRepository.UpdateAsync(account);

        var transaction = new Transaction
        {
            FromCustomer = customer.Id,
            ToCustomer = customer.Id,
            Amount = addMoneyDto.Amount,
            Timestamp = DateTime.UtcNow,
            AccountId = account.Id,
            Type = "ADD_MONEY"
        };

        var createdTransaction = await _transactionRepository.CreateAsync(transaction);
        return _mapper.Map<TransactionDto>(createdTransaction);
    }
}