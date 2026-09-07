from django import forms


class ParticipantForm(forms.Form):
    name = forms.CharField(
        max_length=80,
        strip=True,
        help_text="Use a surname if people share a name.",
    )
