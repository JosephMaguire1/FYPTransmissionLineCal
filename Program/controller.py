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
from ConformalMappingMicrostrip import ConfomalMappingMicrostripCalculate
from ConformalMappingCPW import ConfomalMappingCPWCalculate
from ConformalMappingCPW import ConfomalMappingCPWCalculateGroundLayerIncluded

BAD_REQUEST = 400


@app.route('/')
def Home():
    return View.render()

@app.errorhandler(BAD_REQUEST)
def custom_bad_request(error):
    response = jsonify({'message': error.description})
    response.status_code = BAD_REQUEST
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
    Thickness_Of_Conductor = request.args.get('Thickness_Of_Conductor')
    if heights:
        try:
            heights = [float(x) for x in heights]
        except ValueError:
            abort(BAD_REQUEST, 'Invalid heights: {}'.format(heights))

    if Thickness_Of_Conductor:
        try:
            Thickness_Of_Conductor = float(Thickness_Of_Conductor)
        except ValueError:
            abort(BAD_REQUEST, 'Invalid Thickness_Of_Conductor: '.format(Thickness_Of_Conductor))
    else:
        Thickness_Of_Conductor = 0

    if conducting_trace_layer:
        try:
            conducting_trace_layer = int(conducting_trace_layer)
        except ValueError:
            abort(BAD_REQUEST, 'Invalid conducting_trace_layer: {}'.format(conducting_trace_layer))

    if layers_permittivity:
        try:
            layers_permittivity = [float(x) for x in layers_permittivity]
        except ValueError:
            abort(BAD_REQUEST, 'Invalid layers_permittivity: {}' .format(layers_permittivity))

    heights_below = heights[0:conducting_trace_layer]
    heights_above = heights[conducting_trace_layer:]

    eff_below = layers_permittivity[0:conducting_trace_layer]
    eff_above = layers_permittivity[conducting_trace_layer:]

    if Width_Of_Track:
        try:
            Width_Of_Track = float(Width_Of_Track)
        except ValueError:
            abort(BAD_REQUEST, 'Invalid Width_Of_Track: {}'.format(Width_Of_Track))

    if not heights_above:
        heights_above = [100]

    if not eff_above:
        eff_above = [1]

    if ( heights_below and eff_below and Width_Of_Track ):
        answer = ConfomalMappingMicrostripCalculate(heights_above, heights_below, eff_above, eff_below, Width_Of_Track, Thickness_Of_Conductor)
        return ViewMicrostrip.render(answer, heights, layers_permittivity, Width_Of_Track, Thickness_Of_Conductor)
    else:
        answer = [' ', ' ']
        return ViewMicrostrip.render(answer, heights, layers_permittivity, Width_Of_Track, Thickness_Of_Conductor)

@app.route('/CPW')
def CPW():
        heights = request.args.getlist('layers_heights')
        heights.reverse()
        conducting_trace_layer = request.args.get('conducting_trace_layer')
        grounded_layer = request.args.get('grounded_layer')
        layers_permittivity = request.args.getlist('layers_permittivity')
        layers_permittivity.reverse()
        Width_Of_Track = request.args.get('Width_Of_Track')
        Width_Of_Gap = request.args.get('Width_Of_Gap')
        Width_Of_Ground = request.args.get('Width_Of_Ground')

        if heights:
            try:
                heights = [float(x) for x in heights]
            except ValueError:
                abort(BAD_REQUEST, 'Invalid heights: {}'.format(heights))

        if conducting_trace_layer:
            try:
                conducting_trace_layer = int(conducting_trace_layer)
            except ValueError:
                abort(BAD_REQUEST, 'Invalid conducting_trace_layer: {}'.format(conducting_trace_layer))

        heights_below = heights[0:conducting_trace_layer]
        heights_above = heights[conducting_trace_layer:]
        heights_below.reverse()

        if layers_permittivity:
            try:
                layers_permittivity = [float(x) for x in layers_permittivity]
            except ValueError:
                abort(BAD_REQUEST, 'Invalid layers_permittivity: {}'.format(layers_permittivity))

        eff_below = layers_permittivity[0:conducting_trace_layer]
        eff_above = layers_permittivity[conducting_trace_layer:]
        eff_below.reverse()

        if Width_Of_Track:
            try:
                Width_Of_Track = float(Width_Of_Track)
            except ValueError:
                abort(BAD_REQUEST, 'Invalid Width_Of_Track: {}'.format(Width_Of_Track))

        if Width_Of_Gap:
            try:
                Width_Of_Gap = float(Width_Of_Gap)
            except ValueError:
                abort(BAD_REQUEST, 'Invalid Width_Of_Gap: {}'.format(Width_Of_Gap))

        if Width_Of_Ground:
            try:
                Width_Of_Ground = float(Width_Of_Ground)
            except ValueError:
                abort(BAD_REQUEST, 'Invalid Width_Of_Ground: {}'.format(Width_Of_Ground))

        if not grounded_layer:
            grounded_layer = "No"

        if grounded_layer == "No":
            if ( heights_below and eff_below and Width_Of_Track and Width_Of_Gap and Width_Of_Ground):
                answer = ConfomalMappingCPWCalculate(heights_above, heights_below, eff_above, eff_below, Width_Of_Track, Width_Of_Gap, Width_Of_Ground)
                return ViewCPW.render(answer, heights, layers_permittivity, Width_Of_Track, Width_Of_Gap, Width_Of_Ground)
            else:
                answer = [' ', ' ']
                return ViewCPW.render(answer, heights, layers_permittivity, Width_Of_Track, Width_Of_Gap, Width_Of_Ground)
        else:
            if ( heights_above and heights_below and eff_above and eff_below and Width_Of_Track and Width_Of_Gap and Width_Of_Ground):
                answer = ConfomalMappingCPWCalculateGroundLayerIncluded(heights_above, heights_below, eff_above, eff_below, Width_Of_Track, Width_Of_Gap, Width_Of_Ground)
                return ViewCPW.render(answer, heights, layers_permittivity, Width_Of_Track, Width_Of_Gap, Width_Of_Ground)
            else:
                answer = [' ', ' ']
                return ViewCPW.render(answer, heights, layers_permittivity, Width_Of_Track, Width_Of_Gap, Width_Of_Ground)

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
