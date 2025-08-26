namespace HorizonBank.Core.DTOs;

public class AccountDto
{
    public int Id { get; set; }
    public string AccountNumber { get; set; } = string.Empty;
    public decimal Balance { get; set; }
    public int CustomerId { get; set; }
}

public class CreateAccountDto
{
    public string AccountNumber { get; set; } = string.Empty;
    public decimal Balance { get; set; }
    public int CustomerId { get; set; }
}

public class AddMoneyDto
{
    public int CustomerId { get; set; }
    public decimal Amount { get; set; }
}