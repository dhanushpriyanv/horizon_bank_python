using HorizonBank.Core.Entities;
using HorizonBank.Core.Interfaces;
using HorizonBank.Infrastructure.Data;
using Microsoft.EntityFrameworkCore;

namespace HorizonBank.Infrastructure.Repositories;

public class AccountRepository : IAccountRepository
{
    private readonly HorizonBankDbContext _context;

    public AccountRepository(HorizonBankDbContext context)
    {
        _context = context;
    }

    public async Task<IEnumerable<Account>> GetAllAsync()
    {
        return await _context.Accounts.Include(a => a.Customer).ToListAsync();
    }

    public async Task<Account?> GetByIdAsync(int id)
    {
        return await _context.Accounts
            .Include(a => a.Customer)
            .FirstOrDefaultAsync(a => a.Id == id);
    }

    public async Task<Account?> GetByCustomerIdAsync(int customerId)
    {
        return await _context.Accounts
            .Include(a => a.Customer)
            .FirstOrDefaultAsync(a => a.CustomerId == customerId);
    }

    public async Task<Account?> GetByAccountNumberAsync(string accountNumber)
    {
        return await _context.Accounts
            .Include(a => a.Customer)
            .FirstOrDefaultAsync(a => a.AccountNumber == accountNumber);
    }

    public async Task<Account> CreateAsync(Account account)
    {
        _context.Accounts.Add(account);
        await _context.SaveChangesAsync();
        return account;
    }

    public async Task<Account> UpdateAsync(Account account)
    {
        _context.Entry(account).State = EntityState.Modified;
        await _context.SaveChangesAsync();
        return account;
    }

    public async Task DeleteAsync(int id)
    {
        var account = await _context.Accounts.FindAsync(id);
        if (account != null)
        {
            _context.Accounts.Remove(account);
            await _context.SaveChangesAsync();
        }
    }
}