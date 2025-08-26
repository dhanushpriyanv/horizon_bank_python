using AutoMapper;
using HorizonBank.Core.DTOs;
using HorizonBank.Core.Entities;
using HorizonBank.Core.Exceptions;
using HorizonBank.Core.Interfaces;

namespace HorizonBank.Infrastructure.Services;

public class CustomerService : ICustomerService
{
    private readonly ICustomerRepository _customerRepository;
    private readonly IMapper _mapper;

    public CustomerService(ICustomerRepository customerRepository, IMapper mapper)
    {
        _customerRepository = customerRepository;
        _mapper = mapper;
    }

    public async Task<IEnumerable<CustomerDto>> GetAllCustomersAsync()
    {
        var customers = await _customerRepository.GetAllAsync();
        return _mapper.Map<IEnumerable<CustomerDto>>(customers);
    }

    public async Task<CustomerDto?> GetCustomerByIdAsync(int id)
    {
        var customer = await _customerRepository.GetByIdAsync(id);
        return customer != null ? _mapper.Map<CustomerDto>(customer) : null;
    }

    public async Task<CustomerDto> CreateCustomerAsync(CreateCustomerDto customerDto)
    {
        var customer = _mapper.Map<Customer>(customerDto);
        var createdCustomer = await _customerRepository.CreateAsync(customer);
        return _mapper.Map<CustomerDto>(createdCustomer);
    }

    public async Task<CustomerDto> UpdateCustomerAsync(int id, UpdateCustomerDto customerDto)
    {
        var existingCustomer = await _customerRepository.GetByIdAsync(id);
        if (existingCustomer == null)
        {
            throw new CustomerNotFoundException($"Customer with ID {id} not found");
        }

        _mapper.Map(customerDto, existingCustomer);
        var updatedCustomer = await _customerRepository.UpdateAsync(existingCustomer);
        return _mapper.Map<CustomerDto>(updatedCustomer);
    }

    public async Task DeleteCustomerAsync(int id)
    {
        var customer = await _customerRepository.GetByIdAsync(id);
        if (customer == null)
        {
            throw new CustomerNotFoundException($"Customer with ID {id} not found");
        }

        await _customerRepository.DeleteAsync(id);
    }
}