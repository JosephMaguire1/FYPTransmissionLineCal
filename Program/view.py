from flask import render_template

class View(object):
    @classmethod
    def render(self):
        return render_template("base.html")

class ViewMicrostrip(object):
    @classmethod
    def render(self, answer, heights, layers_permittivity, Width_Of_Track, Thickness_Of_Conductor):
        return render_template("baseMicrostrip.html", answer1=answer, heights=heights, layers_permittivity=layers_permittivity, Width_Of_Track=Width_Of_Track, Thickness_Of_Conductor=Thickness_Of_Conductor)

class ViewCPW(object):
    @classmethod
    def render(self, answer, heights, layers_permittivity, Width_Of_Track, Width_Of_Gap, Width_Of_Ground):
        return render_template("baseCPW.html", answer1=answer, heights=heights, layers_permittivity=layers_permittivity, Width_Of_Track=Width_Of_Track, Width_Of_Gap=Width_Of_Gap, Width_Of_Ground=Width_Of_Ground)

class ViewMicrostripCalculations(object):
    @classmethod
    def render(self):
        return render_template("baseMicrostripCalculations.html")

class ViewCPWCalculations(object):
    @classmethod
    def render(self):
        return render_template("baseCPWcalculation.html")
