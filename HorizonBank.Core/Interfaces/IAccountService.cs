using HorizonBank.Core.DTOs;

namespace HorizonBank.Core.Interfaces;

public interface IAccountService
{
    Task<IEnumerable<AccountDto>> GetAllAccountsAsync();
    Task<AccountDto?> GetAccountByIdAsync(int id);
    Task<AccountDto?> GetAccountByCustomerIdAsync(int customerId);
    Task<AccountDto?> GetAccountByAccountNumberAsync(string accountNumber);
    Task<AccountDto> CreateAccountAsync(CreateAccountDto accountDto);
    Task<AccountDto> AddMoneyAsync(AddMoneyDto addMoneyDto);
    Task DeleteAccountAsync(int id);
}