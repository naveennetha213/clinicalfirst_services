from marshmallow import Schema, fields, validate

class Patient_sub_registration(Schema):
    # patient_id = fields.String(validate=validate.Regexp(r'[A-Za-z0-9]+'))
    patient_age = fields.Integer(required=True)
    patient_exp = fields.Float(required=True)
    patient_gender = fields.String(validate=validate.Regexp(r'^[A-Za-z]+'))
    patient_licnce_num = fields.String(validate=validate.Regexp(r'^[A-Za-z0-9]+'))
    patient_flat_num = fields.String(validate=validate.Regexp(r'^[A-Za-z0-9]+'))
    patient_street_name = fields.String(validate=validate.Regexp(r'^[A-Za-z]+'))
    patient_city_name = fields.String(validate=validate.Regexp(r'^[A-Za-z]+'))
    patient_state_name = fields.String(validate=validate.Regexp(r'^[A-Za-z]+'))
    patient_country_name = fields.String(validate=validate.Regexp(r'^[A-Za-z]+'))
    zipcode = fields.Integer(required=True)
    # patient_approved = fields.String(validate=validate.Regexp(r'(19|20)\d\d[- /.](0[1-9]|1[012])'
    #                                                       r'[- /.](0[1-9]|[12][0-9]|3[01])$'))
    # ip = fields.String(validate=validate.Regexp(r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|'
    #                                             r'[01]?[0-9][0-9]?)$'))
    # date = fields.String(validate=validate.Regexp(r'(19|20)\d\d[- /.](0[1-9]|1[012])'
    #                                                       r'[- /.](0[1-9]|[12][0-9]|3[01])$'))

class Patient_registration(Schema):
    # patient_id = fields.String(validate=validate.Regexp(r'[A-Za-z0-9]+'))
    patient_age = fields.Integer(required=True)
    patient_exp = fields.Float(required=True)
    patient_gender = fields.String(validate=validate.Regexp(r'^[A-Za-z]+'))
    patient_licnce_num = fields.String(validate=validate.Regexp(r'^[A-Za-z0-9]+'))
    patient_flat_num = fields.String(validate=validate.Regexp(r'^[A-Za-z0-9]+'))
    patient_street_name = fields.String(validate=validate.Regexp(r'^[A-Za-z]+'))
    patient_city_name = fields.String(validate=validate.Regexp(r'^[A-Za-z]+'))
    patient_state_name = fields.String(validate=validate.Regexp(r'^[A-Za-z]+'))
    patient_country_name = fields.String(validate=validate.Regexp(r'^[A-Za-z]+'))
    zipcode = fields.Integer(required=True)
    # patient_approved = fields.String(validate=validate.Regexp(r'(19|20)\d\d[- /.](0[1-9]|1[012])'
    #                                                       r'[- /.](0[1-9]|[12][0-9]|3[01])$'))
    # ip = fields.String(validate=validate.Regexp(r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|'
    #                                             r'[01]?[0-9][0-9]?)$'))
    # date = fields.String(validate=validate.Regexp(r'(19|20)\d\d[- /.](0[1-9]|1[012])'
    #                                                       r'[- /.](0[1-9]|[12][0-9]|3[01])$'))

