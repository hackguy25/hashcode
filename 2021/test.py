
import time

primer = "LONG"

fib = lambda num: (lambda f, x: f(f, x))((lambda rec, n: n if n < 2 else rec(rec, n-1) + rec(rec, n-2)), num)
print([fib(i) for i in range(10)])
print("jajc")
test = 9.1
test2 = test + 1
print(test)
print(test2)
print('Erika je kul')
# time.sleep(30)
print(primer)