from app.calculations import * 
import pytest 

@pytest.fixture
def zero_bank_account ():
    return BankAccount()

@pytest.fixture 
def initial_bank_account():
    return BankAccount(50)

@pytest.mark.parametrize("num1,num2,result" ,[
    (1,1,2) , 
    (12,13,25) , 
    (4,5,9)
])
def test_add(num1,num2,result):
    assert add(num1,num2) == result

def test_multiply():
    assert multiply(3,5)  == 15

def test_subtract():
    assert subtract(3,5)  == -2

def test_divide():
    assert divide(15,3)  == 5


def test_initial_bank_account (initial_bank_account):
    assert initial_bank_account.balance == 50 

def test_zero_bank_account(zero_bank_account) :
    assert zero_bank_account.balance == 0 


@pytest.mark.parametrize("deposit,withdraw,balance" , [
    (100,50,50) ,
    (500,1,499),
    (200,100,100)
])
def test_bank_transaction (zero_bank_account , deposit , withdraw , balance):
    bank_account = zero_bank_account
    bank_account.deposit(deposit)
    bank_account.withdraw(withdraw)
    assert bank_account.balance == balance

def test_insufficient_funds (initial_bank_account):
    with pytest.raises(InsufficientFunds):
        initial_bank_account.withdraw(200)

