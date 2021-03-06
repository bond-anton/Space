import unittest
import numpy as np

from BDSpace.Coordinates.transforms import reduce_angle, reduce_angles, unit_vector, angles_between_vectors
from BDSpace.Coordinates.transforms import cartesian_to_spherical_point, spherical_to_cartesian_point
from BDSpace.Coordinates.transforms import cartesian_to_spherical, spherical_to_cartesian
from BDSpace.Coordinates.transforms import cartesian_to_cylindrical_point
from BDSpace.Coordinates.transforms import cartesian_to_cylindrical, cylindrical_to_cartesian
from BDSpace.Coordinates.transforms import cylindrical_to_spherical, spherical_to_cylindrical


class TestTransforms(unittest.TestCase):

    def test_reduce_angle_constant_positive(self):
        angle = 0.1
        self.assertEqual(reduce_angle(angle, keep_sign=True), angle)
        self.assertEqual(reduce_angle(angle, keep_sign=False), angle)
        angle = 1
        self.assertEqual(reduce_angle(angle, keep_sign=True), angle)
        self.assertEqual(reduce_angle(angle, keep_sign=False), angle)

    def test_reduce_angle_constant_negative(self):
        angle = -0.1
        self.assertEqual(reduce_angle(angle, keep_sign=True), angle)
        self.assertEqual(reduce_angle(angle, keep_sign=False), angle + 2 * np.pi)
        angle = -1
        self.assertEqual(reduce_angle(angle, keep_sign=True), angle)
        self.assertEqual(reduce_angle(angle, keep_sign=False), angle + 2 * np.pi)

    def test_reduce_angle_constant_zero(self):
        angle = 0.0
        self.assertEqual(reduce_angle(angle, keep_sign=True), angle)
        self.assertEqual(reduce_angle(angle, keep_sign=False), angle)

    def test_reduce_angle_constant_2pi(self):
        angle = -2 * np.pi
        self.assertEqual(reduce_angle(angle, keep_sign=True), angle)
        self.assertEqual(reduce_angle(angle, keep_sign=False), angle + 2 * np.pi)
        angle = 2 * np.pi
        self.assertEqual(reduce_angle(angle, keep_sign=True), angle)
        self.assertEqual(reduce_angle(angle, keep_sign=False), angle)

    def test_reduce_angle_array(self):
        angle = np.array([0.1, ])
        np.testing.assert_allclose(reduce_angles(angle, keep_sign=True), angle)
        np.testing.assert_allclose(reduce_angles(angle, keep_sign=False), angle)
        angle = np.array([1, ], dtype=np.double)
        np.testing.assert_allclose(reduce_angles(angle, keep_sign=True), angle)
        np.testing.assert_allclose(reduce_angles(angle, keep_sign=False), angle)
        angle = np.array([0.1, -0.2])
        np.testing.assert_allclose(reduce_angles(angle, keep_sign=True), angle)
        angle = np.array([0.1, 0.2])
        np.testing.assert_allclose(reduce_angles(angle, keep_sign=True), angle)
        np.testing.assert_allclose(reduce_angles(angle, keep_sign=False), angle)

    def test_reduce_angle_random_array_positive(self):
        size = 1000
        angle = np.random.random(size) * 2 * np.pi
        full_turns = np.random.randint(0, 101, size=size) * 2 * np.pi * 1
        np.testing.assert_allclose(reduce_angles(angle + full_turns, keep_sign=False),
                                   reduce_angles(angle, keep_sign=False))
        np.testing.assert_allclose(reduce_angles(angle + full_turns, keep_sign=True),
                                   reduce_angles(angle, keep_sign=True))
        np.testing.assert_allclose(reduce_angles(angle + full_turns, keep_sign=True), angle)
        np.testing.assert_allclose(reduce_angles(angle + full_turns, keep_sign=False), angle)

    def test_reduce_angle_random_array_loops(self):
        size = 1000
        angle = (np.random.random(size) - 0.5) * 4 * np.pi
        full_turns = np.random.randint(-100, 101, size=size) * 2 * np.pi * 1
        np.testing.assert_allclose(reduce_angles(angle + full_turns, keep_sign=False),
                                   reduce_angles(angle, keep_sign=False))

    def test_reduce_angle_random_array(self):
        size = 1000
        angle = (np.random.random(size) - 0.5) * 4 * np.pi
        np.testing.assert_allclose(reduce_angles(angle, keep_sign=True), angle)

    def test_unit_vector_1d(self):
        v = 0.1
        with self.assertRaises(TypeError):
            unit_vector(v)
        v = [0.1]
        with self.assertRaises(TypeError):
            unit_vector(v)
        v = np.array([0.1])
        np.testing.assert_allclose(unit_vector(v), np.array([1.0]))

    def test_unit_vector_null_vector(self):
        with self.assertRaises(TypeError):
            unit_vector(0.0)
        max_dimensions = 100
        for dim in range(max_dimensions):
            v = np.zeros(dim)
            np.testing.assert_allclose(unit_vector(v), v)

    def test_unit_vector_random_vector(self):
        max_dimensions = 100
        for dim in range(max_dimensions):
            v = np.random.random(dim+1) * 100
            if np.linalg.norm(v) > 0:
                np.testing.assert_allclose(unit_vector(v), v / np.sqrt(np.dot(v, v)))
            else:
                np.testing.assert_allclose(unit_vector(v), v)

    def test_angle_between_vectors(self):
        v1 = np.array([1, 0, 0], dtype=np.float)
        v2 = np.array([0, 1, 0], dtype=np.float)
        self.assertEqual(angles_between_vectors(v1, v2), np.pi/2)
        self.assertEqual(angles_between_vectors(v1, v1), 0)
        self.assertEqual(angles_between_vectors(v1, -v1), np.pi)
        v2 = np.array([1, 1, 0], dtype=np.float)
        np.testing.assert_allclose(angles_between_vectors(v1, v2), np.pi/4)
        v2 = np.array([1, 1], dtype=np.float)
        np.testing.assert_allclose(angles_between_vectors(v1, v2), np.pi / 4)
        np.testing.assert_allclose(angles_between_vectors(v2, v1), np.pi / 4)

    def test_to_spherical_single_point(self):
        xyz = np.array([1, 0, 0], dtype=np.double)
        np.testing.assert_allclose(cartesian_to_spherical_point(xyz), [1, np.pi / 2, 0], atol=np.finfo(float).eps)
        xyz = np.array([0, 1, 0], dtype=np.double)
        np.testing.assert_allclose(cartesian_to_spherical_point(xyz), [1, np.pi / 2, np.pi / 2], atol=np.finfo(float).eps)
        xyz = np.array([0, 0, 0], dtype=np.double)
        np.testing.assert_allclose(cartesian_to_spherical_point(xyz), [0, 0, 0], atol=np.finfo(float).eps)

    def test_to_spherical_wrong_arguments(self):
        xyz = 0
        self.assertRaises(TypeError, cartesian_to_spherical, xyz)
        xyz = [0, 0]
        self.assertRaises(TypeError, cartesian_to_spherical, xyz)

    def test_to_spherical_and_back_many_points(self):
        points_num = 100
        xyz = ((np.random.random(points_num * 3) - 0.5) * 200).reshape((points_num, 3))
        rtp = cartesian_to_spherical(xyz)
        np.testing.assert_allclose(spherical_to_cartesian(rtp), xyz)

    def test_to_cartesian_single_point(self):
        rtp = np.zeros(3, dtype=np.double)
        np.testing.assert_allclose(spherical_to_cartesian_point(rtp), [0, 0, 0], atol=np.finfo(float).eps)
        rtp = np.array([0, 1, 0], dtype=np.double)
        np.testing.assert_allclose(spherical_to_cartesian_point(rtp), [0, 0, 0], atol=np.finfo(float).eps)
        rtp = np.array([1, 0, 0], dtype=np.double)
        np.testing.assert_allclose(spherical_to_cartesian_point(rtp), [0, 0, 1], atol=np.finfo(float).eps)
        rtp = np.array([1, np.pi/2, 0], dtype=np.double)
        np.testing.assert_allclose(spherical_to_cartesian_point(rtp), [1, 0, 0], atol=np.finfo(float).eps)
        rtp = np.array([1, np.pi, 0], dtype=np.double)
        np.testing.assert_allclose(spherical_to_cartesian_point(rtp), [0, 0, -1], atol=np.finfo(float).eps)

    def test_to_cartesian_wrong_arguments(self):
        rtp = 0
        self.assertRaises(TypeError, spherical_to_cartesian, rtp)
        rtp = [0, 0]
        self.assertRaises(TypeError, spherical_to_cartesian, rtp)

    def test_to_cylindrical_single_point(self):
        xyz = np.array([1, 0, 0], dtype=np.double)
        np.testing.assert_allclose(cartesian_to_cylindrical_point(xyz), [1, 0, 0], atol=np.finfo(float).eps)
        xyz = np.array([0, 1, 0], dtype=np.double)
        np.testing.assert_allclose(cartesian_to_cylindrical_point(xyz), [1, np.pi / 2, 0], atol=np.finfo(float).eps)
        xyz = np.array([1, 0, 1], dtype=np.double)
        np.testing.assert_allclose(cartesian_to_cylindrical_point(xyz), [1, 0, 1], atol=np.finfo(float).eps)
        xyz = np.array([0, 0, 0], dtype=np.double)
        np.testing.assert_allclose(cartesian_to_cylindrical_point(xyz), [0, 0, 0], atol=np.finfo(float).eps)
        xyz = np.array([0, 0, 1], dtype=np.double)
        np.testing.assert_allclose(cartesian_to_cylindrical_point(xyz), [0, 0, 1], atol=np.finfo(float).eps)

    def test_to_cylindrical_and_back_many_points(self):
        points_num = 100
        xyz = ((np.random.random(points_num * 3) - 0.5) * 200).reshape((points_num, 3))
        rpz = cartesian_to_cylindrical(xyz)
        np.testing.assert_allclose(cylindrical_to_cartesian(rpz), xyz)
        rtp = cylindrical_to_spherical(rpz)
        np.testing.assert_allclose(cartesian_to_spherical(xyz), rtp)
        np.testing.assert_allclose(spherical_to_cylindrical(rtp), rpz)
        np.testing.assert_allclose(spherical_to_cartesian(rtp), xyz)
