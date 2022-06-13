# Here, we import the forms, since they are used for routing.
# We also add routing to the InputForm.
from flask import render_template,request, url_for, flash, redirect
from web_for_undercut import app
from web_for_undercut.forms import AlgoInputForm
from web_for_undercut.compute import get_solution
import json
from dataclasses import dataclass, asdict
from typing import Any,List

@dataclass
class AlgoInput:
    items: list[Any]
    preferences_a:str
    preferences_b : str
    agents: List[Any]
    algorithm: str
    
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True)


@app.route('/')
def index():
    return render_template('home.html')

@app.route('/input', methods=['GET', 'POST'])
def input_form():
    form = AlgoInputForm()
    is_submitted = form.validate_on_submit()
    if not is_submitted:
        return render_template('algo.html', form=form)
    else:
        items=form.items.data
        a={}
        b={}
        Alice = form.preferences_a.data
        Bob = form.preferences_b.data
        for index,item in enumerate(items):
            a[item] =int(Alice[index])
            b[item] =int(Bob[index])
        agents=[a,b]
        algo_in = AlgoInput(items=items, preferences_a=Alice,preferences_b=Bob,agents=agents,algorithm=form.algorithm.data)
        return redirect(url_for(output.__name__, algo_in=algo_in.to_json()))


@app.route('/results', methods=['GET', 'POST'])
def output():
    algo_in=json.loads(request.args['algo_in'])
    return render_template('results.html', algo_out=get_solution(algo_in),algo_in=algo_in)
