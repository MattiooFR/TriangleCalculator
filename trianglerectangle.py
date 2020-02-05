# Quick tools I create to calculate things with Khan Academy
import math
import operator
import os.path
from argparse import ArgumentParser


def get_args():
    parser = ArgumentParser()
    parser.add_argument(
        "AB",
        default=None,
        nargs="?",
        help='AB',
        type=float)
    parser.add_argument(
        "BC",
        default=None,
        nargs="?",
        help='BC',
        type=float)
    parser.add_argument(
        "AC",
        default=None,
        nargs="?",
        help='AC',
        type=float)
    parser.add_argument(
        "CAB",
        default=None,
        nargs="?",
        help='CAB',
        type=float)
    parser.add_argument(
        "ABC",
        default=None,
        nargs="?",
        help='ABC',
        type=float)
    parser.add_argument(
        "BCA",
        default=None,
        nargs="?",
        help='BCA',
        type=float)

    args = parser.parse_args()
    return args


class AngleError(Exception):
    pass


class SideError(Exception):
    pass


class TriangleRectangle:
    def __init__(
            self,
            AB=None,
            BC=None,
            AC=None,
            CAB=None,
            ABC=None,
            BCA=None):

        if CAB and CAB > 90:
            self.CAB = ((CAB // 90) + 1) * 90 - CAB
        else:
            self.CAB = CAB
        if ABC and ABC > 90:
            self.ABC = ((ABC // 90) + 1) * 90 - ABC
        else:
            self.ABC = ABC
        if BCA and BCA > 90:
            self.BCA = ((BCA // 90) + 1) * 90 - BCA
        else:
            self.BCA = BCA

        self.rotation = 0

        self.AB = AB
        self.BC = BC
        self.AC = AC

        while not (
                self.AB and self.BC and self.AC and self.CAB and self.ABC and self.BCA):
            if self.CAB == 90:
                if not self.ABC and self.BCA:
                    self.ABC = 90 - self.BCA
                elif self.ABC and not self.BCA:
                    self.BCA = 90 - self.ABC

                if self.ABC > 90:
                    self.rotation =  self.ABC // 90
                else:
                    self.rotation = 0

                if not self.ABC:
                    if self.AB and self.BC:
                        self.ABC = math.asin(math.radians(self.AB / self.BC))
                    elif self.AC and self.BC:
                        self.ABC = math.acos(math.radians(self.AC / self.BC))
                    elif self.AB and self.AC:
                        self.ABC = math.atan(math.radians(self.AB / self.AC))

                if not self.BCA:
                    if self.AC and self.BC:
                        self.BCA = math.asin(math.radians(self.AC / self.BC))
                    elif self.AB and self.BC:
                        self.BCA = math.acos(math.radians(self.AB / self.BC))
                    elif self.AC and self.AB:
                        self.BCA = math.atan(math.radians(self.AC / self.AB))

                if not self.AB:
                    if self.BC and self.ABC:
                        self.AB = math.sin(math.radians(self.ABC)) * self.BC
                    elif self.BC and self.BCA:
                        self.AB = math.cos(math.radians(self.BCA)) * self.BC
                    elif self.AC and self.ABC:
                        self.AB = math.tan(math.radians(self.ABC)) * self.AC
                    elif self.AC and self.BCA:
                        self.AB = self.AC / math.tan(math.radians(self.BCA))

                if not self.BC:
                    if self.AB and self.AC:
                        self.BC = math.sqrt(self.AB**2 + self.AC**2)
                    elif self.ABC and self.AB:
                        self.BC = self.AB / math.sin(math.radians(self.ABC))
                    elif self.ABC and self.AC:
                        self.BC = self.AC / math.cos(math.radians(self.ABC))
                    elif self.BCA and self.AB:
                        self.BC = self.AB / math.cos(math.radians(self.BCA))
                    elif self.BCA and self.AC:
                        self.BC = self.AC / math.sin(math.radians(self.BCA))

                if not self.AC:
                    if self.BC and self.ABC:
                        self.AC = math.cos(math.radians(self.ABC)) * self.BC
                    elif self.BC and self.BCA:
                        self.AC = math.sin(math.radians(self.BCA)) * self.BC
                    elif self.AB and self.BCA:
                        self.AC = math.tan(math.radians(self.BCA)) * self.AB
                    elif self.AB and self.ABC:
                        self.AC = self.AB / math.tan(math.radians(self.ABC))

            if self.ABC == 90:
                if not self.CAB and self.BCA:
                    self.CAB = 90 - self.BCA
                elif self.CAB and not self.BCA:
                    self.BCA = 90 - self.CAB

                if self.BCA > 90:
                    self.rotation =  self.BCA // 90
                else:
                    self.rotation = 0

                if not self.BCA:
                    if self.BC and self.AC:
                        self.BCA = math.asin(math.radians(self.BC / self.AC))
                    elif self.AB and self.AC:
                        self.BCA = math.acos(math.radians(self.AB / self.AC))
                    elif self.BC and self.AB:
                        self.BCA = math.atan(math.radians(self.BC / self.AB))

                if not self.CAB:
                    if self.AB and self.AC:
                        self.CAB = math.asin(math.radians(self.AB / self.AC))
                    elif self.BC and self.AC:
                        self.CAB = math.acos(math.radians(self.BC / self.AC))
                    elif self.AB and self.BC:
                        self.CAB = math.atan(math.radians(self.AB / self.BC))

                if not self.AB:
                    if self.AC and self.CAB:
                        self.AB = math.sin(math.radians(self.CAB)) * self.AC
                    elif self.AC and self.BCA:
                        self.AB = math.cos(math.radians(self.BCA)) * self.AC
                    elif self.BC and self.CAB:
                        self.AB = math.tan(math.radians(self.CAB)) * self.BC
                    elif self.BC and self.BCA:
                        self.AB = self.BC / math.tan(math.radians(self.BCA))

                if not self.AC:
                    if self.AB and self.BC:
                        self.AC = math.sqrt(self.AB**2 + self.BC**2)
                    elif self.BCA and self.BC:
                        self.AC = self.BC / math.sin(math.radians(self.BCA))
                    elif self.CAB and self.BC:
                        self.AC = self.BC / math.cos(math.radians(self.CAB))
                    elif self.BCA and self.AB:
                        self.AC = self.AB / math.cos(math.radians(self.BCA))
                    elif self.CAB and self.AB:
                        self.AC = self.AB / math.sin(math.radians(self.CAB))

                if not self.BC:
                    if self.AC and self.CAB:
                        self.BC = math.cos(math.radians(self.CAB)) * self.AC
                    elif self.AC and self.BCA:
                        self.BC = math.sin(math.radians(self.BCA)) * self.AC
                    elif self.AB and self.BCA:
                        self.BC = math.tan(math.radians(self.BCA)) * self.AB
                    elif self.AB and self.CAB:
                        self.BC = self.AB / math.tan(math.radians(self.CAB))

            if self.BCA == 90:
                if not self.ABC and self.CAB:
                    self.ABC = 90 - self.CAB
                elif self.ABC and not self.CAB:
                    self.CAB = 90 - self.ABC

                if self.CAB > 90:
                    self.rotation =  self.CAB // 90
                else:
                    self.rotation = 0

                if not self.CAB:
                    if self.BC and self.AB:
                        self.CAB = math.asin(math.radians(self.BC / self.AB))
                    elif self.AC and self.AB:
                        self.CAB = math.acos(math.radians(self.AC / self.AB))
                    elif self.BC and self.AC:
                        self.CAB = math.atan(math.radians(self.BC / self.AC))

                if not self.ABC:
                    if self.AC and self.AB:
                        self.ABC = math.asin(math.radians(self.AC / self.AB))
                    elif self.BC and self.AB:
                        self.ABC = math.acos(math.radians(self.BC / self.AB))
                    elif self.AC and self.BC:
                        self.ABC = math.atan(math.radians(self.AC / self.BC))

                if not self.AB:
                    if self.BC and self.AC:
                        self.AB = math.sqrt(self.BC**2 + self.AC**2)
                    elif self.CAB and self.BC:
                        self.AB = self.BC / math.sin(math.radians(self.CAB))
                    elif self.CAB and self.AC:
                        self.AB = self.AC / math.cos(math.radians(self.CAB))
                    elif self.ABC and self.BC:
                        self.AB = self.BC / math.cos(math.radians(self.ABC))
                    elif self.ABC and self.AC:
                        self.AB = self.AC / math.sin(math.radians(self.ABC))

                if not self.BC:
                    if self.AB and self.CAB:
                        self.BC = math.sin(math.radians(self.CAB)) * self.AB
                    elif self.AB and self.ABC:
                        self.BC = math.cos(math.radians(self.ABC)) * self.AB
                    elif self.AC and self.CAB:
                        self.BC = math.tan(math.radians(self.CAB)) * self.AC
                    elif self.AC and self.ABC:
                        self.BC = self.AC / math.tan(math.radians(self.ABC))

                if not self.AC:
                    if self.AB and self.CAB:
                        self.AC = math.cos(math.radians(self.CAB)) * self.AB
                    elif self.AB and self.ABC:
                        self.AC = math.sin(math.radians(self.ABC)) * self.AB
                    elif self.BC and self.ABC:
                        self.AC = math.tan(math.radians(self.ABC)) * self.BC
                    elif self.BC and self.CAB:
                        self.AC = self.BC / math.tan(math.radians(self.CAB))

        if self.rotation == 0:
            self.vector = (round(self.AC, 2), round(self.BC, 2))
        elif self.rotation == 1:
            self.vector = (0 - round(self.AC, 2), round(self.BC, 2))
        elif self.rotation == 2:
            self.vector = (0 - round(self.BC, 2), 0 - round(self.AC, 2))
        elif self.rotation == 3:
            self.vector = (round(self.AC, 2), 0 - round(self.BC, 2))

        self.angles = {
            "CAB": round(self.CAB, 2),
            "ABC": round(self.ABC, 2),
            "BCA": round(self.BCA, 2)
        }
        self.sides = {
            "AB": round(self.AB, 2),
            "BC": round(self.BC, 2),
            "AC": round(self.AC, 2)
        }

    def _get_angles(self):
        return self.angles

    def _set_angles(self, angles):
        for name, angle in angles.items:
            if (not isinstance(angle, int) or not isinstance(
                    angle, float)) or angle > 90:
                raise AngleError(angle)
        else:
            self.angles[name] = angles

    #angles = property(_get_angles, _set_angles)

    def _get_sides(self):
        return self.sides

    def _set_sides(self, sides):
        for name, side in sides.items:
            if (not isinstance(side, int) or not isinstance(
                    side, float)) or side <= 0:
                raise SideError(side)
        else:
            self.angles[name] = sides

    #sides = property(_get_sides, _set_sides)

    def __repr__(self):
        return f"The angles are {self.angles} and the sides length are {self.sides}."

    def get_vector(self):
        return f"Vector : {self.vector}"

    def __add__(self, other):
        return f"Vector : {tuple(map(operator.add, self.vector, other.vector))}"

    def __sub__(self, other):
        return f"Vector : {tuple(map(operator.sub, self.vector, other.vector))}"


def main():
    args = get_args()
    if not (not args.AB and not args.ABC and not args.AC and not args.BC and not args.BCA and not args.CAB):
        triangle = TriangleRectangle(
            args.AB,
            args.BC,
            args.AC,
            args.CAB,
            args.ABC,
            args.BCA)
        print(triangle)
    else:
        triangle2 = TriangleRectangle(8, 0, 0, 100, 0, 90)
        triangle1 = TriangleRectangle(3, 0, 0, 210, 0, 90)
        print(triangle1 + triangle2)


if __name__ == '__main__':
    main()
