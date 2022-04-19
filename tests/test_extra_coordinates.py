import pytest
import numpy as np
import unyt as u
from toysnap import present_particle_types

reltol = 1.01  # allow some wiggle room for floating point roundoff
abstol_c = 1 * u.pc  # less than this is ~0
abstol_v = 10 * u.m / u.s  # less than this is ~0


class TestCartesianCoordinates:

    @pytest.mark.parametrize("particle_name", present_particle_types.values())
    @pytest.mark.parametrize(
        "coordinate_name, mask",
        (
            ('x', np.s_[:, 0]),
            ('y', np.s_[:, 1]),
            ('z', np.s_[:, 2]),
            ('xyz', np.s_[...])
        )
    )
    @pytest.mark.parametrize(
        "coordinate_type, tol",
        (
            ('coordinates', abstol_c),
            ('velocities', abstol_v),
        )
    )
    def test_cartesian_coordinates(self, sg, particle_name, coordinate_name,
                                   mask, coordinate_type, tol):
        coordinate = getattr(
            getattr(sg, particle_name),
            coordinate_type
        )[mask]
        cartesian_coordinate = getattr(
            getattr(
                getattr(sg, particle_name),
                f'cartesian_{coordinate_type}'
            ),
            coordinate_name
        )
        assert(np.abs(cartesian_coordinate - coordinate) <= tol).all()
