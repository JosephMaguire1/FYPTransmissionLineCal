from flask import (
    Flask,
    request,
    abort,
    jsonify,
)

app = Flask(__name__, static_url_path='/static')

from view import View
from view import ViewMicrostrip
from view import ViewCPW
from view import ViewMicrostripCalculations
from view import ViewCPWCalculations
from collections import defaultdict
from ConformalMappingMicrostrip1 import ConfomalMappingMicrostripCalculate
from ConformalMappingCPW1 import ConfomalMappingCPWCalculate


@app.route('/')
def Home():
    return View.render()

@app.errorhandler(400)
def custom400(error):
    response = jsonify({'message': error.description})
    response.status_code = 404
    response.status = 'error.Bad Request'
    return response

@app.route('/Microstrip')
def Microstrip():
    heights = request.args.getlist('layers_heights')
    heights.reverse()
    conducting_trace_layer = request.args.get('conducting_trace_layer')
    layers_permittivity = request.args.getlist('layers_permittivity')
    layers_permittivity.reverse()
    Width_Of_Track = request.args.get('Width_Of_Track')

    if heights:
        try:
            heights = [float(x) for x in heights]
        except ValueError:
            abort(404)

    if conducting_trace_layer:
        try:
            conducting_trace_layer = int(conducting_trace_layer)
        except ValueError:
            abort(404)

    heights_below = heights[0:conducting_trace_layer]
    heights_above = heights[conducting_trace_layer:]
    print("heights_above is:", heights_above)
    print("heights_below is:", heights_below)

    if layers_permittivity:
        try:
            layers_permittivity = [float(x) for x in layers_permittivity]
        except ValueError:
            abort(404)

    eff_below = layers_permittivity[0:conducting_trace_layer]
    eff_above = layers_permittivity[conducting_trace_layer:]
    print("eff_above is:", eff_above)
    print("eff_below is:", eff_below)

    if Width_Of_Track:
        try:
            Width_Of_Track = float(Width_Of_Track)
        except ValueError:
            abort(404)

    # if statments check
    if ( heights_above and heights_below and eff_above and eff_below and Width_Of_Track ):
        answer = ConfomalMappingMicrostripCalculate(heights_above, heights_below, eff_above, eff_below, Width_Of_Track)
        return ViewMicrostrip.render(answer)
    else:
        answer = [' ', ' ']
        return ViewMicrostrip.render(answer)

@app.route('/CPW')
def CPW():
        heights = request.args.getlist('layers_heights')
        heights.reverse()
        conducting_trace_layer = request.args.get('conducting_trace_layer')
        layers_permittivity = request.args.getlist('layers_permittivity')
        layers_permittivity.reverse()
        Width_Of_Track = request.args.get('Width_Of_Track')
        Width_Of_Gap = request.args.get('Width_Of_Gap')
        Width_Of_Ground = request.args.get('Width_Of_Ground')
        if heights:
            try:
                heights = [float(x) for x in heights]
            except ValueError:
                abort(404)

        heights_below = heights[0:conducting_trace_layer]
        heights_above = heights[conducting_trace_layer:]
        print("heights_above is:", heights_above)
        print("heights_below is:", heights_below)

        if layers_permittivity:
            try:
                layers_permittivity = [float(x) for x in layers_permittivity]
            except ValueError:
                abort(404)

        eff_below = layers_permittivity[0:conducting_trace_layer]
        eff_above = layers_permittivity[conducting_trace_layer:]
        print("eff_above is:", eff_above)
        print("eff_below is:", eff_below)

        if Width_Of_Track:
            try:
                Width_Of_Track = float(Width_Of_Track)
            except ValueError:
                abort(404)
        if Width_Of_Gap:
            try:
                Width_Of_Gap = float(Width_Of_Gap)
            except ValueError:
                abort(404)
        if Width_Of_Ground:
            try:
                Width_Of_Ground = float(Width_Of_Ground)
            except ValueError:
                abort(404)
        if ( heights_above and heights_below and eff_above and eff_below and Width_Of_Track and Width_Of_Gap and Width_Of_Ground):
            answer = ConfomalMappingCPWCalculate(heights_above, heights_below, eff_above, eff_below, Width_Of_Track, Width_Of_Gap, Width_Of_Ground)
            return ViewCPW.render(answer)
        else:
            answer = [' ', ' ']
            return ViewCPW.render(answer)


@app.route('/MicrostripCalculations')
def MicrostripCalculations():
    return ViewMicrostripCalculations.render()

@app.route('/CPWCalculations')
def CPWCalculations():
    return ViewCPWCalculations.render()

if __name__=="__main__":
    app.run(debug=True)
    app.run(TEMPLATES_AUTO_RELOAD=True)
    app.run(SEND_FILE_MAX_AGE_DEFAULT=True)
