# print("Hello, World!")

user_input = input("이름을 입력하세요: ")
print("안녕하세요, " + user_input + "님!")

# If-else
user_input = input("나이를 입력하세요: ")
if user_input.isdigit():
    age = int(user_input)
    print("성인" if age >= 20 else "미성년자")
    if age < 20:
        print("당신은 미성년자입니다.")
    else:
        print("당신은 성인입니다.")

if age < 18 or age >= 60:
    print("할인 대상입니다.")



score = 85
if (score >= 80 and score < 90) or score == 100:
    print("우수")

is_logged_in = False
if not is_logged_in:
    print("로그인이 필요합니다.")

# for
for i in range(5):
    print("i =", i)

# while
count = 0
while count < 3:
    print("count =", count)
    count += 1

# Arrays and Lists
fruits = ["apple", "banana", "cherry"]
fruits.append("grape") # 추가
new_fruit = input("추가할 과일 이름을 입력하세요: ")
fruits.append(new_fruit)
print(fruits[0])       # apple
print("현재 과일 목록:")
for fruit in fruits:   # 모든 과일 출력
    print("-", fruit)
search_fruits = input("찾을 과일 이름: ")
if search_fruits in fruits:
    print(search_fruits, "이(가) 리스트에 있습니다.")
else:
    print(search_fruits, "은(는) 리스트에 없습니다.")
# fruits.remove("cherry")   # 첫 번째 cherry만 삭제됨
# removed = fruits.pop(1)   # fruits index 1의 항목 삭제 ('banana')를 리턴. removed에는 'banana'가 저장됨. fruits에서는 'banana'가 삭제됨.
# del fruits[0] # index 0의 항목 삭제
fruits.sort() # 오름차순 정렬
print(fruits)
fruits.sort(reverse=True) # 내림차순 정렬
print(fruits)
new_list = sorted(fruits) # 새로운 정렬된 리스트 생성 (원본 fruits는 변경되지 않음)
new_list_desc = sorted(fruits, reverse=True) # 새로운 정렬된 리스트 생성 (원본 fruits는 변경되지 않음)
print(new_list)
print(new_list_desc)
unique = list(set(fruits)) # 중복 제거 후 리스트로 변환
unique_sorted = sorted(set(fruits)) # 중복 제거 후 정렬된 리스트 생성
print(unique_sorted)
# 순서 유지하면서 중복 제거
unique = []
for fruit in fruits:
    if fruit not in unique:
        unique.append(fruit)


# Dictionaries
person = {"name": "Bob", "age": 30}
print(person["name"])

# Functions
def greet(name):
    print("Hello,", name)
greet("Alice")

# Classes and Objects
class Person:
    def __init__(self, name):
        self.name = name

    def say_hello(self):
        print("Hi, I'm", self.name)

p = Person("John")
p.say_hello()

# Exception Handling
try:
    x = int(input("숫자 입력: "))
    print(10 / x)
except ValueError:
    print("숫자가 아닙니다.")
except ZeroDivisionError:
    print("0으로 나눌 수 없습니다.")