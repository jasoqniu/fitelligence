from flask import Flask, render_template, request, redirect, url_for
import google.generativeai as palm

palm.configure(api_key="AIzaSyCYwcNtj9pXV0m8aa7ixIQAVjApDayiVTQ")
model = {"model": "models/chat-bison-001"}

app = Flask(__name__)
arr=[]
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/personal_info', methods=['POST'])
def personal_info():
    name = request.form['name']
    return render_template('personal_info.html', name=name)

@app.route('/fitness_level', methods=['POST'])
def fitness_level():
    age = request.form['age'] #arr[0]
    arr.append(age)
    weight = request.form['weight'] #arr[1] 
    arr.append(weight)
    height = request.form['height'] #arr[2]
    arr.append(height)
    gender = request.form['gender'] #arr[3]
    arr.append(gender)
    return render_template('fitness_level.html', age=age, weight=weight, height=height, gender=gender)

@app.route('/results', methods=['POST'])
def results():
    weight = float(request.form['weight'])
    height = float(request.form['height']) / 100
    bmi = round(weight / (height ** 2), 2)
    
    if bmi < 18.5:
        health_status = "Underweight"
        calorie_recommendation = "2500 calories/day"
    elif bmi < 24.9:
        health_status = "Normal weight"
        calorie_recommendation = "2000 calories/day"
    else:
        health_status = "Overweight"
        calorie_recommendation = "1800 calories/day"

    
    
    return render_template('results.html', bmi=bmi, health_status=health_status, calorie_recommendation=calorie_recommendation)

@app.route('/goals', methods=['POST'])
def goals():
    return render_template('goals.html')

@app.route('/plan', methods=['GET','POST'])
def plan():
    q=f"give me workout plan for a person that has age of {arr[0]}, weight is {arr[1]} kilograms, height is {arr[2]} cm, and my gender is {arr[3]},"
    response = palm.chat(**model, messages=q)
    return render_template('plan.html', workout_plan=response.last)

@app.route('/meal_plan', methods=['GET'])
def meal_plan():
    q = "give me meal plan"
    response = palm.chat(**model, messages=q)
    meal_plan = response.last
    return render_template('meal_plan.html', meal_plan=meal_plan)


if __name__ == '__main__':
    app.run()
