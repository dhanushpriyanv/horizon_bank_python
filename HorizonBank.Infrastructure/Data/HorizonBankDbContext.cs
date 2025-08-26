using HorizonBank.Core.Entities;
using Microsoft.EntityFrameworkCore;

namespace HorizonBank.Infrastructure.Data;

public class HorizonBankDbContext : DbContext
{
    public HorizonBankDbContext(DbContextOptions<HorizonBankDbContext> options) : base(options) { }

    public DbSet<Customer> Customers { get; set; }
    public DbSet<Account> Accounts { get; set; }
    public DbSet<Transaction> Transactions { get; set; }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);

        // Configure sequences for Oracle
        modelBuilder.HasSequence<int>("CUSTOMER_SEQ")
            .StartsAt(1)
            .IncrementsBy(1);

        modelBuilder.HasSequence<int>("ACCOUNT_SEQ")
            .StartsAt(1)
            .IncrementsBy(1);

        modelBuilder.HasSequence<int>("TRANSACTION_SEQ")
            .StartsAt(1)
            .IncrementsBy(1);

        // Configure entities to use sequences
        modelBuilder.Entity<Customer>()
            .Property(e => e.Id)
            .HasDefaultValueSql("CUSTOMER_SEQ.NEXTVAL");

        modelBuilder.Entity<Account>()
            .Property(e => e.Id)
            .HasDefaultValueSql("ACCOUNT_SEQ.NEXTVAL");

        modelBuilder.Entity<Transaction>()
            .Property(e => e.Id)
            .HasDefaultValueSql("TRANSACTION_SEQ.NEXTVAL");

        // Configure relationships
        modelBuilder.Entity<Account>()
            .HasOne(a => a.Customer)
            .WithMany(c => c.Accounts)
            .HasForeignKey(a => a.CustomerId)
            .OnDelete(DeleteBehavior.Cascade);

        modelBuilder.Entity<Transaction>()
            .HasOne(t => t.Account)
            .WithMany(a => a.Transactions)
            .HasForeignKey(t => t.AccountId)
            .OnDelete(DeleteBehavior.Cascade);

        modelBuilder.Entity<Transaction>()
            .HasOne(t => t.FromCustomerRef)
            .WithMany(c => c.FromTransactions)
            .HasForeignKey(t => t.FromCustomer)
            .OnDelete(DeleteBehavior.NoAction);

        modelBuilder.Entity<Transaction>()
            .HasOne(t => t.ToCustomerRef)
            .WithMany(c => c.ToTransactions)
            .HasForeignKey(t => t.ToCustomer)
            .OnDelete(DeleteBehavior.NoAction);

        // Configure decimal precision
        modelBuilder.Entity<Account>()
            .Property(a => a.Balance)
            .HasPrecision(18, 2);

        modelBuilder.Entity<Transaction>()
            .Property(t => t.Amount)
            .HasPrecision(18, 2);
    }
}