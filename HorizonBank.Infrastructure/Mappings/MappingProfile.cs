using AutoMapper;
using HorizonBank.Core.DTOs;
using HorizonBank.Core.Entities;

namespace HorizonBank.Infrastructure.Mappings;

public class MappingProfile : Profile
{
    public MappingProfile()
    {
        // Customer mappings
        CreateMap<Customer, CustomerDto>();
        CreateMap<CreateCustomerDto, Customer>();
        CreateMap<UpdateCustomerDto, Customer>();

        // Account mappings
        CreateMap<Account, AccountDto>();
        CreateMap<CreateAccountDto, Account>();

        // Transaction mappings
        CreateMap<Transaction, TransactionDto>()
            .ForMember(dest => dest.FromCustomerRef, opt => opt.MapFrom(src => src.FromCustomerRef))
            .ForMember(dest => dest.ToCustomerRef, opt => opt.MapFrom(src => src.ToCustomerRef));
    }
}