using HorizonBank.Core.DTOs;

namespace HorizonBank.Core.Interfaces;

public interface ITransactionService
{
    Task<IEnumerable<TransactionDto>> GetAllTransactionsAsync();
    Task<TransactionDto?> GetTransactionByIdAsync(int id);
    Task<IEnumerable<TransactionDto>> GetTransactionsByCustomerIdAsync(int customerId);
    Task<TransactionDto> TransferMoneyAsync(TransferMoneyDto transferDto);
    Task<TransactionDto> PayBillAsync(BillPayDto billPayDto);
    Task<TransactionDto> AddMoneyAsync(AddMoneyDto addMoneyDto);
}