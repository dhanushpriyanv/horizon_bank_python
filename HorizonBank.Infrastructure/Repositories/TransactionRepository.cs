using HorizonBank.Core.Entities;
using HorizonBank.Core.Interfaces;
using HorizonBank.Infrastructure.Data;
using Microsoft.EntityFrameworkCore;

namespace HorizonBank.Infrastructure.Repositories;

public class TransactionRepository : ITransactionRepository
{
    private readonly HorizonBankDbContext _context;

    public TransactionRepository(HorizonBankDbContext context)
    {
        _context = context;
    }

    public async Task<IEnumerable<Transaction>> GetAllAsync()
    {
        return await _context.Transactions
            .Include(t => t.Account)
            .Include(t => t.FromCustomerRef)
            .Include(t => t.ToCustomerRef)
            .ToListAsync();
    }

    public async Task<Transaction?> GetByIdAsync(int id)
    {
        return await _context.Transactions
            .Include(t => t.Account)
            .Include(t => t.FromCustomerRef)
            .Include(t => t.ToCustomerRef)
            .FirstOrDefaultAsync(t => t.Id == id);
    }

    public async Task<IEnumerable<Transaction>> GetByCustomerIdAsync(int customerId)
    {
        return await _context.Transactions
            .Include(t => t.Account)
            .Include(t => t.FromCustomerRef)
            .Include(t => t.ToCustomerRef)
            .Where(t => t.Account.CustomerId == customerId)
            .OrderByDescending(t => t.Timestamp)
            .ToListAsync();
    }

    public async Task<Transaction> CreateAsync(Transaction transaction)
    {
        _context.Transactions.Add(transaction);
        await _context.SaveChangesAsync();
        return transaction;
    }

    public async Task DeleteAsync(int id)
    {
        var transaction = await _context.Transactions.FindAsync(id);
        if (transaction != null)
        {
            _context.Transactions.Remove(transaction);
            await _context.SaveChangesAsync();
        }
    }
}