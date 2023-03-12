from src.solid.open_closed.example import JuniorTeacher


def test_can_instantiate_junior_teacher() -> None:
    # when
    teacher = JuniorTeacher(name="Maurice Moss")

    # then
    assert isinstance(teacher, JuniorTeacher)


def test_junior_teacher_can_teach_maths() -> None:
    # given
    teacher_name = "Maurice Moss"
    teacher = JuniorTeacher(name=teacher_name)

    # when
    lesson = teacher.teach_class("maths")

    # then
    assert lesson == f"{teacher_name} is teaching algebra!"
