using HorizonBank.Core.Entities;

namespace HorizonBank.Core.Interfaces;

public interface IAccountRepository
{
    Task<IEnumerable<Account>> GetAllAsync();
    Task<Account?> GetByIdAsync(int id);
    Task<Account?> GetByCustomerIdAsync(int customerId);
    Task<Account?> GetByAccountNumberAsync(string accountNumber);
    Task<Account> CreateAsync(Account account);
    Task<Account> UpdateAsync(Account account);
    Task DeleteAsync(int id);
}