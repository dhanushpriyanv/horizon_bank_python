using HorizonBank.Core.DTOs;
using HorizonBank.Core.Exceptions;
using HorizonBank.Core.Interfaces;
using Microsoft.AspNetCore.Mvc;

namespace HorizonBank.API.Controllers;

[ApiController]
[Route("api/[controller]")]
public class TransactionsController : ControllerBase
{
    private readonly ITransactionService _transactionService;

    public TransactionsController(ITransactionService transactionService)
    {
        _transactionService = transactionService;
    }

    [HttpGet]
    public async Task<ActionResult<IEnumerable<TransactionDto>>> GetAll()
    {
        var transactions = await _transactionService.GetAllTransactionsAsync();
        return Ok(transactions);
    }

    [HttpGet("{id}")]
    public async Task<ActionResult<TransactionDto>> GetById(int id)
    {
        var transaction = await _transactionService.GetTransactionByIdAsync(id);
        if (transaction == null)
            return NotFound();

        return Ok(transaction);
    }

    [HttpGet("customer/{customerId}")]
    public async Task<ActionResult<IEnumerable<TransactionDto>>> GetByCustomerId(int customerId)
    {
        var transactions = await _transactionService.GetTransactionsByCustomerIdAsync(customerId);
        return Ok(transactions);
    }

    [HttpPost]
    public async Task<ActionResult<TransactionDto>> TransferMoney(TransferMoneyDto transferDto)
    {
        try
        {
            var transaction = await _transactionService.TransferMoneyAsync(transferDto);
            return Ok(transaction);
        }
        catch (AccountNotFoundException ex)
        {
            return NotFound(new { error = ex.Message });
        }
        catch (InsufficientFundsException ex)
        {
            return BadRequest(new { error = ex.Message });
        }
    }

    [HttpPost("bill-pay")]
    public async Task<ActionResult<TransactionDto>> PayBill(BillPayDto billPayDto)
    {
        try
        {
            var transaction = await _transactionService.PayBillAsync(billPayDto);
            return Ok(transaction);
        }
        catch (CustomerNotFoundException ex)
        {
            return NotFound(new { error = ex.Message });
        }
        catch (AccountNotFoundException ex)
        {
            return NotFound(new { error = ex.Message });
        }
        catch (InsufficientFundsException ex)
        {
            return BadRequest(new { error = ex.Message });
        }
    }

    [HttpPost("add-money")]
    public async Task<ActionResult<TransactionDto>> AddMoney(AddMoneyDto addMoneyDto)
    {
        try
        {
            var transaction = await _transactionService.AddMoneyAsync(addMoneyDto);
            return Ok(transaction);
        }
        catch (CustomerNotFoundException ex)
        {
            return NotFound(new { error = ex.Message });
        }
        catch (AccountNotFoundException ex)
        {
            return NotFound(new { error = ex.Message });
        }
    }
}