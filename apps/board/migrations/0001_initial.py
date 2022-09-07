# Generated by Django 4.1 on 2022-09-07 03:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='등록 날짜')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정 날짜')),
                ('title', models.CharField(max_length=20, verbose_name='제목')),
                ('content', models.CharField(max_length=200, verbose_name='본문')),
                ('author', models.CharField(max_length=10, verbose_name='글쓴이')),
                ('password', models.BinaryField()),
                ('is_deleted', models.BooleanField(default=False, verbose_name='삭제 여부')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
