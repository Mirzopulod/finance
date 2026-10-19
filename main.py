import abc


class Account:
    def __init__(self, name, owner, balance) -> None:
        self.name = name
        self.__owner = owner
        self.balance = balance

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if value != '':
            self.__name = value
        else:
            print("Имя не может быть пустым")

    @property
    def owner(self):
        return self.__owner

    @property
    def balance(self):
        return self.__balance

    @balance.setter
    def balance(self, num):
        if num >= 0:
            self.__balance = num
        else:
            print("Баланс не может быть отрицательным")

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
        else:
            print("Пополнение должно быть больше нуля")

    def withdraw(self, amount):
        if amount > 0 and self.__balance >= amount:
            self.__balance -= amount
            return True
        else:
            print("Списание должно быть больше нуля и меньше текущего баланса")
            return False


class Transaction(abc.ABC):
    def __init__(self, amount, data, description = '') -> None:
        self.__amount = amount
        self.__data = data
        self.__description = description

    @property
    def amount(self):
        return self.__amount

    @property
    def data(self):
        return self.__data

    @property
    def description(self):
        return self.__description

    @abc.abstractmethod
    def execute(self):
        pass


class Income(Transaction):
    def __init__(self, amount, account, data, description = '') -> None:
        super().__init__(amount, data, description)
        self.__account = account

    def execute(self):
        self.__account.deposit(self.amount)


class Expense(Transaction):
    def __init__(self, amount, account, data, description = '') -> None:
        super().__init__(amount, data, description)
        self.__account = account

    def execute(self):
        self.__account.withdraw(self.amount)


class Transfer(Transaction):
    def __init__(self, amount, account1, account2, data, description = '') -> None:
        super().__init__(amount, data, description)
        self.__account1 = account1
        self.__account2 = account2

    def execute(self):
        if self.__account1.withdraw(self.amount):
            self.__account2.deposit(self.amount)


class FinanceManager:
    def __init__(self) -> None:
        self.__accounts = []
        self.__history = []

    def account(self, account):
        self.__accounts.append(account)

    def operation(self, operation):
        self.__history.append(operation)


def main():
    pass


if __name__ == "__main__":
    main()
