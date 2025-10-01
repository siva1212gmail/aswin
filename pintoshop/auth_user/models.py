from django.db import models

class User(models.Model):
    lng_User_ID = models.BigAutoField(primary_key=True)
    str_Username = models.CharField(max_length=100)
    str_Full_Name = models.CharField(max_length=200)
    str_Hashed_Password = models.CharField(max_length=255, null=True, blank=True)
    bln_IsPassword_Expiry = models.BooleanField()
    dte_Last_Pwd_Modified_Date = models.DateTimeField(null=True, blank=True)
    dte_Modified_Date = models.DateTimeField(null=True, blank=True)
    dte_Created_Date = models.DateTimeField(auto_now_add=True)
    dte_Last_Login = models.DateTimeField(null=True, blank=True)
    bln_IsActive = models.BooleanField(default=True)
    bln_IsDeleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'tbl_User'

    def __str__(self):
        return self.str_Username


class UserContact(models.Model):
    lng_User_ContactID = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='lng_User_ID')
    str_Contact_Type = models.CharField(max_length=50)
    str_Contact_Value = models.CharField(max_length=150)
    bln_IsPrimary = models.BooleanField(null=True, blank=True)
    bln_IsVerified = models.BooleanField()
    dte_Verified_Date = models.DateTimeField(null=True, blank=True)
    dte_Modified_Date = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'tbl_User_Contact'
    def __str__(self):
        return self.user

class UserAddress(models.Model):
    lng_User_Address_ID = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='lng_User_ID')
    str_Address_Line1 = models.CharField(max_length=255)
    str_Address_Line2 = models.CharField(max_length=255, null=True, blank=True)
    str_City = models.CharField(max_length=100)
    str_State = models.CharField(max_length=100)
    str_Country = models.CharField(max_length=100)
    str_Zip_Code = models.CharField(max_length=20)
    dte_Added_Date = models.DateTimeField()
    bln_IsPrimary = models.BooleanField()
    dte_Modified_Date = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'tbl_User_Address'
    def __str__(self):
        return self.user


class UserSSO(models.Model):
    lng_User_SSO_ID = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='lng_User_ID')
    str_SSO_Provider = models.CharField(max_length=50)
    str_Provider_User_ID = models.CharField(max_length=200)
    str_Email = models.CharField(max_length=150)
    dte_Linked_Date = models.DateTimeField()
    bln_IsActive = models.BooleanField(default=True)
    dte_Modified_Date = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'tbl_User_SSO'
    def __str__(self):
        return self.user


class OTPVerification(models.Model):
    lng_OTP_ID = models.BigAutoField(primary_key=True)
    str_Contact_Value = models.CharField(max_length=150)
    str_OTP_Code = models.CharField(max_length=10)
    dte_Sent_Time = models.DateTimeField()

    class Meta:
        db_table = 'tbl_OTP_Verification'
    def __str__(self):
        return self.dte_Sent_Time
