using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace HorizonBank.Core.Entities;

[Table("TRANSACTIONS")]
public class Transaction
{
    [Key]
    [Column("ID")]
    [DatabaseGenerated(DatabaseGeneratedOption.Identity)]
    public int Id { get; set; }

    [Column("AMOUNT")]
    [Required]
    public decimal Amount { get; set; }

    [Column("TIMESTAMP")]
    [Required]
    public DateTime Timestamp { get; set; } = DateTime.UtcNow;

    [Column("TYPE")]
    [Required]
    [MaxLength(20)]
    public string Type { get; set; } = string.Empty;

    [Column("ACCOUNT_ID")]
    [Required]
    public int AccountId { get; set; }

    [Column("FROM_CUSTOMER")]
    public int? FromCustomer { get; set; }

    [Column("TO_CUSTOMER")]
    public int? ToCustomer { get; set; }

    [ForeignKey("AccountId")]
    public virtual Account Account { get; set; } = null!;

    [ForeignKey("FromCustomer")]
    public virtual Customer? FromCustomerRef { get; set; }

    [ForeignKey("ToCustomer")]
    public virtual Customer? ToCustomerRef { get; set; }
}