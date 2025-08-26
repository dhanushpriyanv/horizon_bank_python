namespace HorizonBank.Core.DTOs;

public class CustomerDto
{
    public int Id { get; set; }
    public string CustomerName { get; set; } = string.Empty;
}

public class CreateCustomerDto
{
    public string CustomerName { get; set; } = string.Empty;
}

public class UpdateCustomerDto
{
    public string CustomerName { get; set; } = string.Empty;
}