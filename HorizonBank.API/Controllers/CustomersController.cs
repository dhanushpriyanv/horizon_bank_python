using HorizonBank.Core.DTOs;
using HorizonBank.Core.Exceptions;
using HorizonBank.Core.Interfaces;
using Microsoft.AspNetCore.Mvc;

namespace HorizonBank.API.Controllers;

[ApiController]
[Route("api/[controller]")]
public class CustomersController : ControllerBase
{
    private readonly ICustomerService _customerService;

    public CustomersController(ICustomerService customerService)
    {
        _customerService = customerService;
    }

    [HttpGet]
    public async Task<ActionResult<IEnumerable<CustomerDto>>> GetAll()
    {
        var customers = await _customerService.GetAllCustomersAsync();
        return Ok(customers);
    }

    [HttpGet("{id}")]
    public async Task<ActionResult<CustomerDto>> GetById(int id)
    {
        try
        {
            var customer = await _customerService.GetCustomerByIdAsync(id);
            if (customer == null)
                return NotFound();

            return Ok(customer);
        }
        catch (CustomerNotFoundException)
        {
            return NotFound();
        }
    }

    [HttpPost]
    public async Task<ActionResult<CustomerDto>> Create(CreateCustomerDto customerDto)
    {
        var customer = await _customerService.CreateCustomerAsync(customerDto);
        return CreatedAtAction(nameof(GetById), new { id = customer.Id }, customer);
    }

    [HttpPut("{id}")]
    public async Task<ActionResult<CustomerDto>> Update(int id, UpdateCustomerDto customerDto)
    {
        try
        {
            var updatedCustomer = await _customerService.UpdateCustomerAsync(id, customerDto);
            return Ok(updatedCustomer);
        }
        catch (CustomerNotFoundException)
        {
            return NotFound();
        }
    }

    [HttpDelete("{id}")]
    public async Task<IActionResult> Delete(int id)
    {
        try
        {
            await _customerService.DeleteCustomerAsync(id);
            return Ok(new { message = "Customer deleted successfully" });
        }
        catch (CustomerNotFoundException)
        {
            return NotFound();
        }
    }
}