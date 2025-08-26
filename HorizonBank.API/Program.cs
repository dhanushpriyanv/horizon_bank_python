using HorizonBank.API.Middleware;
using HorizonBank.Infrastructure;
using HorizonBank.Infrastructure.Data;
using Microsoft.EntityFrameworkCore;
using Serilog;

var builder = WebApplication.CreateBuilder(args);

// Add Serilog
Log.Logger = new LoggerConfiguration()
    .WriteTo.Console()
    .WriteTo.File("logs/horizonbank-.txt", rollingInterval: RollingInterval.Day)
    .CreateLogger();

builder.Host.UseSerilog();

// Add services to the container.
builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

// Add CORS
builder.Services.AddCors(options =>
{
    options.AddDefaultPolicy(policy =>
    {
        policy.WithOrigins("http://localhost:5173")
              .AllowAnyHeader()
              .AllowAnyMethod()
              .AllowCredentials();
    });
});

// Add Infrastructure services
builder.Services.AddInfrastructure(builder.Configuration);

var app = builder.Build();

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

// Initialize database
using (var scope = app.Services.CreateScope())
{
    var context = scope.ServiceProvider.GetRequiredService<HorizonBankDbContext>();
    await context.Database.EnsureCreatedAsync();
    
    // Seed data if needed
    await SeedData(context);
}

app.UseMiddleware<ExceptionMiddleware>();

app.UseCors();

app.UseHttpsRedirection();

app.UseAuthorization();

app.MapControllers();

// Health check endpoint
app.MapGet("/api/health/db", async (HorizonBankDbContext context) =>
{
    try
    {
        await context.Database.ExecuteSqlRawAsync("SELECT 'Oracle OK' AS status FROM dual");
        return Results.Ok(new { status = "Oracle OK" });
    }
    catch (Exception ex)
    {
        return Results.Problem(detail: ex.Message, statusCode: 500);
    }
});

app.Run();

static async Task SeedData(HorizonBankDbContext context)
{
    if (!context.Customers.Any())
    {
        var customers = new[]
        {
            new HorizonBank.Core.Entities.Customer { CustomerName = "John Doe" },
            new HorizonBank.Core.Entities.Customer { CustomerName = "Jane Smith" },
            new HorizonBank.Core.Entities.Customer { CustomerName = "Peter Jones" },
            new HorizonBank.Core.Entities.Customer { CustomerName = "Charlie" }
        };

        context.Customers.AddRange(customers);
        await context.SaveChangesAsync();

        var accounts = new[]
        {
            new HorizonBank.Core.Entities.Account { AccountNumber = "1001", Balance = 100000.00m, CustomerId = customers[0].Id },
            new HorizonBank.Core.Entities.Account { AccountNumber = "1002", Balance = 100000.00m, CustomerId = customers[1].Id },
            new HorizonBank.Core.Entities.Account { AccountNumber = "1003", Balance = 100000.00m, CustomerId = customers[2].Id },
            new HorizonBank.Core.Entities.Account { AccountNumber = "1004", Balance = 100000.00m, CustomerId = customers[3].Id }
        };

        context.Accounts.AddRange(accounts);
        await context.SaveChangesAsync();
    }
}