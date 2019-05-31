import pytest
from .helpers import *

import BondGraphTools as bgt


def test_make_diode():

    d = bgt.new("Di", library="elec", value={"Is": 5*10**-6})
    # todo: fix this
    # assert d.metamodel == "Di"
    assert len(d.ports) == 1
    assert d.params["Is"]["value"] == 5*10**-6


def test_diode_model():

    d = bgt.new("Di", library="elec", value=[1, 1, 1])

    assert not d.control_vars

    assert sym_set_eq(d.constitutive_relations, {'f_0 - exp(e_0) +1'})
