using HorizonBank.Core.Entities;

namespace HorizonBank.Core.Interfaces;

public interface ITransactionRepository
{
    Task<IEnumerable<Transaction>> GetAllAsync();
    Task<Transaction?> GetByIdAsync(int id);
    Task<IEnumerable<Transaction>> GetByCustomerIdAsync(int customerId);
    Task<Transaction> CreateAsync(Transaction transaction);
    Task DeleteAsync(int id);
}