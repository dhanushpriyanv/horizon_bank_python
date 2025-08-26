namespace HorizonBank.Core.DTOs;

public class TransactionDto
{
    public int Id { get; set; }
    public decimal Amount { get; set; }
    public DateTime Timestamp { get; set; }
    public string Type { get; set; } = string.Empty;
    public int AccountId { get; set; }
    public int? FromCustomer { get; set; }
    public int? ToCustomer { get; set; }
    public CustomerDto? FromCustomerRef { get; set; }
    public CustomerDto? ToCustomerRef { get; set; }
}

public class TransferMoneyDto
{
    public int FromCustomerId { get; set; }
    public int ToCustomerId { get; set; }
    public decimal Amount { get; set; }
}

public class BillPayDto
{
    public int CustomerId { get; set; }
    public string BillType { get; set; } = string.Empty;
    public string AccountNumber { get; set; } = string.Empty;
    public decimal Amount { get; set; }
}