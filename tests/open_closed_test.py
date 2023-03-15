from src.solid.open_closed.example import JuniorTeacher, Maths, Science, SeniorTeacher


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


def test_junior_teacher_can_teach_science() -> None:
    # given
    teacher_name = "Maurice Moss"
    teacher = JuniorTeacher(name=teacher_name)

    # when
    lesson = teacher.teach_class("science")

    # then
    assert lesson == f"{teacher_name} is teaching particle physics!"


def test_can_instantiate_senior_teacher() -> None:
    # when
    subject = Maths()
    teacher = SeniorTeacher(name="Maurice Moss", subject=subject)

    # then
    assert isinstance(teacher, SeniorTeacher)


def test_senior_teacher_can_teach_maths() -> None:
    # given
    teacher_name = "Maurice Moss"
    subject = Maths()
    teacher = SeniorTeacher(name=teacher_name, subject=subject)

    # when
    lesson = teacher.teach_class()

    # then
    assert lesson == f"{teacher_name} is teaching algebra!"


def test_senior_teacher_can_teach_science() -> None:
    # given
    teacher_name = "Maurice Moss"
    subject = Science()
    teacher = SeniorTeacher(name=teacher_name, subject=subject)

    # when
    lesson = teacher.teach_class()

    # then
    assert lesson == f"{teacher_name} is teaching particle physics!"
