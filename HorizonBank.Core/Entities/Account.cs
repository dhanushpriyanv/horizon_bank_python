using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace HorizonBank.Core.Entities;

[Table("ACCOUNTS")]
public class Account
{
    [Key]
    [Column("ID")]
    [DatabaseGenerated(DatabaseGeneratedOption.Identity)]
    public int Id { get; set; }

    [Column("ACCOUNT_NUMBER")]
    [Required]
    [MaxLength(20)]
    public string AccountNumber { get; set; } = string.Empty;

    [Column("BALANCE")]
    [Required]
    public decimal Balance { get; set; }

    [Column("CUSTOMER_ID")]
    [Required]
    public int CustomerId { get; set; }

    [ForeignKey("CustomerId")]
    public virtual Customer Customer { get; set; } = null!;

    public virtual ICollection<Transaction> Transactions { get; set; } = new List<Transaction>();
}