using HorizonBank.Core.DTOs;
using HorizonBank.Core.Exceptions;
using HorizonBank.Core.Interfaces;
using Microsoft.AspNetCore.Mvc;

namespace HorizonBank.API.Controllers;

[ApiController]
[Route("api/[controller]")]
public class AccountsController : ControllerBase
{
    private readonly IAccountService _accountService;

    public AccountsController(IAccountService accountService)
    {
        _accountService = accountService;
    }

    [HttpGet]
    public async Task<ActionResult<IEnumerable<AccountDto>>> GetAll()
    {
        var accounts = await _accountService.GetAllAccountsAsync();
        return Ok(accounts);
    }

    [HttpGet("{id}")]
    public async Task<ActionResult<AccountDto>> GetById(int id)
    {
        var account = await _accountService.GetAccountByIdAsync(id);
        if (account == null)
            return NotFound();

        return Ok(account);
    }

    [HttpGet("customer/{customerId}")]
    public async Task<ActionResult<AccountDto>> GetByCustomerId(int customerId)
    {
        var account = await _accountService.GetAccountByCustomerIdAsync(customerId);
        if (account == null)
            return NotFound();

        return Ok(account);
    }

    [HttpGet("username")]
    public async Task<ActionResult<AccountDto>> GetByUsername([FromQuery] string username)
    {
        var account = await _accountService.GetAccountByAccountNumberAsync(username);
        if (account == null)
            return NotFound();

        return Ok(account);
    }

    [HttpPost("create")]
    public async Task<ActionResult<AccountDto>> Create(CreateAccountDto accountDto)
    {
        try
        {
            var account = await _accountService.CreateAccountAsync(accountDto);
            return CreatedAtAction(nameof(GetById), new { id = account.Id }, account);
        }
        catch (CustomerNotFoundException ex)
        {
            return BadRequest(new { error = ex.Message });
        }
    }

    [HttpPost("add-money")]
    public async Task<ActionResult<AccountDto>> AddMoney(AddMoneyDto addMoneyDto)
    {
        try
        {
            var updatedAccount = await _accountService.AddMoneyAsync(addMoneyDto);
            return Ok(updatedAccount);
        }
        catch (AccountNotFoundException ex)
        {
            return NotFound(new { error = ex.Message });
        }
    }
}