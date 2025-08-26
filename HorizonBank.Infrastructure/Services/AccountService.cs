using AutoMapper;
using HorizonBank.Core.DTOs;
using HorizonBank.Core.Entities;
using HorizonBank.Core.Exceptions;
using HorizonBank.Core.Interfaces;

namespace HorizonBank.Infrastructure.Services;

public class AccountService : IAccountService
{
    private readonly IAccountRepository _accountRepository;
    private readonly ICustomerRepository _customerRepository;
    private readonly IMapper _mapper;

    public AccountService(IAccountRepository accountRepository, ICustomerRepository customerRepository, IMapper mapper)
    {
        _accountRepository = accountRepository;
        _customerRepository = customerRepository;
        _mapper = mapper;
    }

    public async Task<IEnumerable<AccountDto>> GetAllAccountsAsync()
    {
        var accounts = await _accountRepository.GetAllAsync();
        return _mapper.Map<IEnumerable<AccountDto>>(accounts);
    }

    public async Task<AccountDto?> GetAccountByIdAsync(int id)
    {
        var account = await _accountRepository.GetByIdAsync(id);
        return account != null ? _mapper.Map<AccountDto>(account) : null;
    }

    public async Task<AccountDto?> GetAccountByCustomerIdAsync(int customerId)
    {
        var account = await _accountRepository.GetByCustomerIdAsync(customerId);
        return account != null ? _mapper.Map<AccountDto>(account) : null;
    }

    public async Task<AccountDto?> GetAccountByAccountNumberAsync(string accountNumber)
    {
        var account = await _accountRepository.GetByAccountNumberAsync(accountNumber);
        return account != null ? _mapper.Map<AccountDto>(account) : null;
    }

    public async Task<AccountDto> CreateAccountAsync(CreateAccountDto accountDto)
    {
        var customer = await _customerRepository.GetByIdAsync(accountDto.CustomerId);
        if (customer == null)
        {
            throw new CustomerNotFoundException($"Customer with ID {accountDto.CustomerId} not found");
        }

        var account = _mapper.Map<Account>(accountDto);
        var createdAccount = await _accountRepository.CreateAsync(account);
        return _mapper.Map<AccountDto>(createdAccount);
    }

    public async Task<AccountDto> AddMoneyAsync(AddMoneyDto addMoneyDto)
    {
        var account = await _accountRepository.GetByCustomerIdAsync(addMoneyDto.CustomerId);
        if (account == null)
        {
            throw new AccountNotFoundException($"Account for customer {addMoneyDto.CustomerId} not found");
        }

        account.Balance += addMoneyDto.Amount;
        var updatedAccount = await _accountRepository.UpdateAsync(account);
        return _mapper.Map<AccountDto>(updatedAccount);
    }

    public async Task DeleteAccountAsync(int id)
    {
        var account = await _accountRepository.GetByIdAsync(id);
        if (account == null)
        {
            throw new AccountNotFoundException($"Account with ID {id} not found");
        }

        await _accountRepository.DeleteAsync(id);
    }
}