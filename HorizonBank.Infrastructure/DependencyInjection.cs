using HorizonBank.Core.Interfaces;
using HorizonBank.Infrastructure.Data;
using HorizonBank.Infrastructure.Mappings;
using HorizonBank.Infrastructure.Repositories;
using HorizonBank.Infrastructure.Services;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;

namespace HorizonBank.Infrastructure;

public static class DependencyInjection
{
    public static IServiceCollection AddInfrastructure(this IServiceCollection services, IConfiguration configuration)
    {
        // Database
        services.AddDbContext<HorizonBankDbContext>(options =>
            options.UseOracle(configuration.GetConnectionString("DefaultConnection")));

        // Repositories
        services.AddScoped<ICustomerRepository, CustomerRepository>();
        services.AddScoped<IAccountRepository, AccountRepository>();
        services.AddScoped<ITransactionRepository, TransactionRepository>();

        // Services
        services.AddScoped<ICustomerService, CustomerService>();
        services.AddScoped<IAccountService, AccountService>();
        services.AddScoped<ITransactionService, TransactionService>();

        // AutoMapper
        services.AddAutoMapper(typeof(MappingProfile));

        return services;
    }
}