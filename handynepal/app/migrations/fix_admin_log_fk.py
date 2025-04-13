from django.db import migrations


class Migration(migrations.Migration):
    """
    This migration fixes the foreign key constraint in the django_admin_log table
    to point to the custom user model instead of the default auth_user table.
    """

    dependencies = [
        ('app', '0007_rename_name_artisan_first_name_artisan_artisan_type_and_more'),
        ('admin', '0003_logentry_add_action_flag_choices'),
    ]

    operations = [
        migrations.RunSQL(
            # Forward SQL: Update the foreign key constraint
            """
            ALTER TABLE django_admin_log
            DROP CONSTRAINT IF EXISTS django_admin_log_user_id_c564eba6_fk_auth_user_id;
            
            ALTER TABLE django_admin_log
            ADD CONSTRAINT django_admin_log_user_id_fk
            FOREIGN KEY (user_id) REFERENCES app_user(id) DEFERRABLE INITIALLY DEFERRED;
            """,
            # Reverse SQL: Restore the original constraint (if needed)
            """
            ALTER TABLE django_admin_log
            DROP CONSTRAINT IF EXISTS django_admin_log_user_id_fk;
            
            ALTER TABLE django_admin_log
            ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id
            FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;
            """
        ),
    ] 