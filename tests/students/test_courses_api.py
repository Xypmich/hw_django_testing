import pytest

from students.models import Course, Student
from rest_framework.test import APIClient
from model_bakery import baker


@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def course_factory():
    def c_factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return c_factory

@pytest.fixture
def student_factory():
    def s_factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return s_factory


@pytest.mark.django_db
def test_get_one_course(client, course_factory):
    courses = course_factory(_quantity=10)
    response = client.get(f'/api/v1/courses/{courses[5].id}/')
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == courses[5].id


@pytest.mark.django_db
def test_get_course_list(client, course_factory):
    courses = course_factory(_quantity=10)
    response = client.get('/api/v1/courses/')
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(courses)


@pytest.mark.django_db
def test_get_course_filtered_by_id(client, course_factory):
    courses = course_factory(_quantity=10)
    response = client.get(f'/api/v1/courses/?id={courses[5].id}')
    assert response.status_code == 200
    data = response.json()
    assert data[0]['id'] == courses[5].id


@pytest.mark.django_db
def test_get_course_filtered_by_name(client, course_factory):
    courses = course_factory(_quantity=10)
    response = client.get(f'/api/v1/courses/?name={courses[5].name}')
    assert response.status_code == 200
    data = response.json()
    assert data[0]['name'] == courses[5].name

@pytest.mark.django_db
def test_course_create(client):
    count = Course.objects.count()
    response = client.post('/api/v1/courses/', data={'name': 'Mega_course_v1'})
    assert response.status_code == 201
    assert Course.objects.count() == count + 1

@pytest.mark.django_db
def test_course_update(client, course_factory):
    courses = course_factory(_quantity=10)
    response = client.patch(f'/api/v1/courses/{courses[5].id}/', data={'name': 'Mega_course_v2'})
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == 'Mega_course_v2'

@pytest.mark.django_db
def test_course_delete(client, course_factory):
    courses = course_factory(_quantity=1)
    response = client.delete(f'/api/v1/courses/{courses[0].id}/')
    assert response.status_code == 204
    assert Course.objects.count() == 0
