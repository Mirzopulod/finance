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
            raise ValueError("Имя не может быть пустым")

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
            raise ValueError("Баланс не может быть отрицательным")

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

    def __str__(self):
        return f"счёт: {self.name}, владелец: {self.owner}, баланс: {self.balance}"


class Transaction(abc.ABC):
    @staticmethod
    def is_valid_amount(amount):
        return amount > 0

    def __init__(self, amount, data, description = '') -> None:
        if not Transaction.is_valid_amount(amount):
            raise ValueError("Сумма должна быть больше нуля")
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

    def __eq__(self, other) -> bool:
        if not isinstance(other, Transaction):
            return False
        if type(self) != type(other):
            return False
        return self.amount == other.amount

    def __lt__(self, other):
        if type(self) != type(other):
            raise TypeError("Нельзя сравнивать разные типы операций")
        return self.amount < other.amount

    def __gt__(self, other):
        if type(self) != type(other):
            raise TypeError("Нельзя сравнивать разные типы операций")
        return self.amount > other.amount

    def __bool__(self):
        return self.amount > 0


class Income(Transaction):
    def __init__(self, amount, account, data, description = '') -> None:
        super().__init__(amount, data, description)
        self.__account = account

    def execute(self):
        self.__account.deposit(self.amount)
        return True

    def __str__(self):
        return f"[{self.data}] поступление: {self.amount} на счёт {self.__account.owner} {self.description}"

class Expense(Transaction):
    def __init__(self, amount, account, data, description = '') -> None:
        super().__init__(amount, data, description)
        self.__account = account

    def execute(self):
        return self.__account.withdraw(self.amount)

    def __str__(self):
        return f"[{self.data}] списание: {self.amount} со счёта {self.__account.owner} {self.description}"


class Transfer(Transaction):
    def __init__(self, amount, account1, account2, data, description = '') -> None:
        super().__init__(amount, data, description)
        if account1 is account2:
            raise ValueError("Нельзя переводить самому себе")
        self.__account1 = account1
        self.__account2 = account2

    def execute(self):
        if self.__account1.withdraw(self.amount):
            self.__account2.deposit(self.amount)
            return True
        return False

    def __str__(self):
        return f"[{self.data}] перевод: {self.amount} с {self.__account1.owner} на {self.__account2.owner} {self.description}"


class FinanceManager:
    app_name = "Finance Manager"
    max_accounts = 5

    def __init__(self) -> None:
        self.__accounts = []
        self.__history = []

    def account(self, account):
        if account in self.__accounts:
            print("Этот аккаунт ранее был добавлен")
        elif len(self.__accounts) >= self.max_accounts:
            print("Достигнут предел добавление аккаунта")
        else:
            self.__accounts.append(account)

    def operation(self, operation):
        if operation.execute():
            self.__history.append(operation)
        else:
            print("Операция не выполнена (Недостаточно средств или ошибка)")

    def show_accounts(self):
        for acc in self.__accounts:
            print(acc)

    def show_history(self):
        for op in self.__history:
            print(op)

    def __contains__(self, operation):
        return operation in self.__history

    def __getitem__(self, index):
        return self.__history[index]


def main():
    manager = FinanceManager()
    acc1 = Account("Дебетовый счет", "Макс", 1000)
    acc2 = Account("Дебетовый счет", "Алексей", 0)
    acc3 = acc1
    manager.account(acc3)
    manager.account(acc1)
    manager.account(acc2)

    op = Income(500, acc1, "2023-10-01", "На еду")
    manager.operation(op)

    op = Expense(200, acc1, "2023-10-02")
    manager.operation(op)

    op = Transfer(300, acc1, acc2, "2023-10-03", "Спасибо за поездку")
    manager.operation(op)

    print(acc1.balance, acc2.balance)

    op = Transfer(5000, acc1, acc2, "2023-10-03")
    manager.operation(op)

    manager.show_accounts()
    manager.show_history()

if __name__ == "__main__":
    main()
