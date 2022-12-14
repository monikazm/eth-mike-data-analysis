from mike_analysis.core.sqlite_migrator import SQLiteMigrator
from mike_analysis.core.constants import AssessmentState


def migrate_specified_frontend_content(migrator: SQLiteMigrator, study_cfg):
    # Handles all imports specified in the configuration

    def migrate_frontend_tables(migrator: SQLiteMigrator, study_cfg):
        for table in study_cfg.IMPORT_TABLES:
            if table == 'Assessment':
                migrator.migrate_table_and_index(
                    table, study_cfg.IMPORT_TABLES[table], f'State == {AssessmentState.Finished} AND IsTrialRun IS FALSE')
            else:
                migrator.migrate_table_and_index(
                    table, study_cfg.IMPORT_TABLES[table])
        for assessment_table in study_cfg.IMPORT_ASSESSMENT_TABLES:
            assessment_table = assessment_table + 'Result'
            migrator.migrate_table_and_index(
                assessment_table, (assessment_table + '_AssessmentId'))
        for therapy_table in study_cfg.IMPORT_THERAPY_TABLES:
            therapy_table = therapy_table + 'Result'
            migrator.migrate_table_and_index(
                therapy_table, (therapy_table + '_ExerciseId'))

    migrate_frontend_tables(migrator, study_cfg)

    def migrate_frontend_views(migrator: SQLiteMigrator, study_cfg):
        if study_cfg.IMPORT_ASSESSMENT_RESULTS_FULL_VIEW:
            for assessment_view in study_cfg.IMPORT_ASSESSMENT_TABLES:
                assessment_view = assessment_view + 'ResultFull'
                migrator.migrate_table_index_or_view(
                    assessment_view, overwrite=True)
        if study_cfg.IMPORT_ASSESSMENT_RESULTS_AGGREGATE_VIEW:
            assert study_cfg.IMPORT_ASSESSMENT_RESULTS_FULL_VIEW, \
                "IMPORT_ASSESSMENT_RESULTS_FULL_VIEW must be enabled for this functionality."
            for assessment_view in study_cfg.IMPORT_ASSESSMENT_TABLES:
                assessment_view = assessment_view + 'ResultAggregate'
                migrator.migrate_table_index_or_view(
                    assessment_view, overwrite=True)
        if study_cfg.IMPORT_THERAPY_RESULTS_FULL_VIEW:
            for therapy_view in study_cfg.IMPORT_THERAPY_TABLES:
                therapy_view = therapy_view + 'ResultFull'
                migrator.migrate_table_index_or_view(
                    therapy_view, overwrite=True)
        if study_cfg.IMPORT_THERAPY_RESULTS_AGGREGATE_VIEW:
            assert study_cfg.IMPORT_THERAPY_RESULTS_FULL_VIEW, \
                "IMPORT_THERAPY_RESULTS_FULL_VIEW must be enabled for this functionality."
            for therapy_view in study_cfg.IMPORT_THERAPY_TABLES:
                therapy_view = therapy_view + 'ResultAggregate'
                migrator.migrate_table_index_or_view(
                    therapy_view, overwrite=True)

    migrate_frontend_views(migrator, study_cfg)
