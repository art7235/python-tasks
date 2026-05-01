def balans():
	balans = 1000

	string = int(input("выберите действие: "))

	while string != 0:
		if string == 1:
			print(f"на вашес счету: {balans}")

		if string == 2:
			balans += int(input("Введите сумму:"))

		if string == 3:
			a = int(input("Введите сумму:"))
			if balans - a >= 0:
				balans -= a
			else:
				print("Недостаточно средств")

		string =  int(input("выберите действие: "))


print(balans())