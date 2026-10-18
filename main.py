import abc


class Account:
    def __init__(self, id, name, balance) -> None:
        self.__id = id
        self.__name = name
        self.__balance = balance


class Transaction(abc.ABC):
    pass


class Income(Transaction):
    pass


class Expance(Transaction):
    pass


class Transfer(Transaction):
    pass


class FinanceManager:
    pass


def main():
    pass


if __name__ == "__main__":
    main()
