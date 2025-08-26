using HorizonBank.Core.DTOs;

namespace HorizonBank.Core.Interfaces;

public interface ICustomerService
{
    Task<IEnumerable<CustomerDto>> GetAllCustomersAsync();
    Task<CustomerDto?> GetCustomerByIdAsync(int id);
    Task<CustomerDto> CreateCustomerAsync(CreateCustomerDto customerDto);
    Task<CustomerDto> UpdateCustomerAsync(int id, UpdateCustomerDto customerDto);
    Task DeleteCustomerAsync(int id);
}