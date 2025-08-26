using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace HorizonBank.Core.Entities;

[Table("CUSTOMERS")]
public class Customer
{
    [Key]
    [Column("ID")]
    [DatabaseGenerated(DatabaseGeneratedOption.Identity)]
    public int Id { get; set; }

    [Column("CUSTOMER_NAME")]
    [Required]
    [MaxLength(100)]
    public string CustomerName { get; set; } = string.Empty;

    public virtual ICollection<Account> Accounts { get; set; } = new List<Account>();
    public virtual ICollection<Transaction> FromTransactions { get; set; } = new List<Transaction>();
    public virtual ICollection<Transaction> ToTransactions { get; set; } = new List<Transaction>();
}