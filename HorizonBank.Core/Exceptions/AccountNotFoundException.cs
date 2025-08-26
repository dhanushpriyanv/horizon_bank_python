namespace HorizonBank.Core.Exceptions;

public class AccountNotFoundException : Exception
{
    public AccountNotFoundException(string message) : base(message) { }
    public AccountNotFoundException(string message, Exception innerException) : base(message, innerException) { }
}