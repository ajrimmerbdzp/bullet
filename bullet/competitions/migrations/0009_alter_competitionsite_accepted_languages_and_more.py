# Generated by Django 4.0.4 on 2022-06-06 13:14

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("competitions", "0008_alter_competition_branch"),
    ]

    operations = [
        migrations.AlterField(
            model_name="competitionsite",
            name="accepted_languages",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(
                    choices=[
                        ("af", "Afrikaans"),
                        ("ar", "Arabic"),
                        ("ar-dz", "Algerian Arabic"),
                        ("ast", "Asturian"),
                        ("az", "Azerbaijani"),
                        ("bg", "Bulgarian"),
                        ("be", "Belarusian"),
                        ("bn", "Bengali"),
                        ("br", "Breton"),
                        ("bs", "Bosnian"),
                        ("ca", "Catalan"),
                        ("cs", "Czech"),
                        ("cy", "Welsh"),
                        ("da", "Danish"),
                        ("de", "German"),
                        ("dsb", "Lower Sorbian"),
                        ("el", "Greek"),
                        ("en", "English"),
                        ("en-au", "Australian English"),
                        ("en-gb", "British English"),
                        ("eo", "Esperanto"),
                        ("es", "Spanish"),
                        ("es-ar", "Argentinian Spanish"),
                        ("es-co", "Colombian Spanish"),
                        ("es-mx", "Mexican Spanish"),
                        ("es-ni", "Nicaraguan Spanish"),
                        ("es-ve", "Venezuelan Spanish"),
                        ("et", "Estonian"),
                        ("eu", "Basque"),
                        ("fa", "Persian"),
                        ("fi", "Finnish"),
                        ("fr", "French"),
                        ("fy", "Frisian"),
                        ("ga", "Irish"),
                        ("gd", "Scottish Gaelic"),
                        ("gl", "Galician"),
                        ("he", "Hebrew"),
                        ("hi", "Hindi"),
                        ("hr", "Croatian"),
                        ("hsb", "Upper Sorbian"),
                        ("hu", "Hungarian"),
                        ("hy", "Armenian"),
                        ("ia", "Interlingua"),
                        ("id", "Indonesian"),
                        ("ig", "Igbo"),
                        ("io", "Ido"),
                        ("is", "Icelandic"),
                        ("it", "Italian"),
                        ("ja", "Japanese"),
                        ("ka", "Georgian"),
                        ("kab", "Kabyle"),
                        ("kk", "Kazakh"),
                        ("km", "Khmer"),
                        ("kn", "Kannada"),
                        ("ko", "Korean"),
                        ("ky", "Kyrgyz"),
                        ("lb", "Luxembourgish"),
                        ("lt", "Lithuanian"),
                        ("lv", "Latvian"),
                        ("mk", "Macedonian"),
                        ("ml", "Malayalam"),
                        ("mn", "Mongolian"),
                        ("mr", "Marathi"),
                        ("ms", "Malay"),
                        ("my", "Burmese"),
                        ("nb", "Norwegian Bokmål"),
                        ("ne", "Nepali"),
                        ("nl", "Dutch"),
                        ("nn", "Norwegian Nynorsk"),
                        ("os", "Ossetic"),
                        ("pa", "Punjabi"),
                        ("pl", "Polish"),
                        ("pt", "Portuguese"),
                        ("pt-br", "Brazilian Portuguese"),
                        ("ro", "Romanian"),
                        ("ru", "Russian"),
                        ("sk", "Slovak"),
                        ("sl", "Slovenian"),
                        ("sq", "Albanian"),
                        ("sr", "Serbian"),
                        ("sr-latn", "Serbian Latin"),
                        ("sv", "Swedish"),
                        ("sw", "Swahili"),
                        ("ta", "Tamil"),
                        ("te", "Telugu"),
                        ("tg", "Tajik"),
                        ("th", "Thai"),
                        ("tk", "Turkmen"),
                        ("tr", "Turkish"),
                        ("tt", "Tatar"),
                        ("udm", "Udmurt"),
                        ("uk", "Ukrainian"),
                        ("ur", "Urdu"),
                        ("uz", "Uzbek"),
                        ("vi", "Vietnamese"),
                        ("zh-hans", "Simplified Chinese"),
                        ("zh-hant", "Traditional Chinese"),
                    ],
                    max_length=10,
                ),
                size=None,
            ),
        ),
        migrations.AlterField(
            model_name="localizedproblem",
            name="language",
            field=models.TextField(
                choices=[
                    ("af", "Afrikaans"),
                    ("ar", "Arabic"),
                    ("ar-dz", "Algerian Arabic"),
                    ("ast", "Asturian"),
                    ("az", "Azerbaijani"),
                    ("bg", "Bulgarian"),
                    ("be", "Belarusian"),
                    ("bn", "Bengali"),
                    ("br", "Breton"),
                    ("bs", "Bosnian"),
                    ("ca", "Catalan"),
                    ("cs", "Czech"),
                    ("cy", "Welsh"),
                    ("da", "Danish"),
                    ("de", "German"),
                    ("dsb", "Lower Sorbian"),
                    ("el", "Greek"),
                    ("en", "English"),
                    ("en-au", "Australian English"),
                    ("en-gb", "British English"),
                    ("eo", "Esperanto"),
                    ("es", "Spanish"),
                    ("es-ar", "Argentinian Spanish"),
                    ("es-co", "Colombian Spanish"),
                    ("es-mx", "Mexican Spanish"),
                    ("es-ni", "Nicaraguan Spanish"),
                    ("es-ve", "Venezuelan Spanish"),
                    ("et", "Estonian"),
                    ("eu", "Basque"),
                    ("fa", "Persian"),
                    ("fi", "Finnish"),
                    ("fr", "French"),
                    ("fy", "Frisian"),
                    ("ga", "Irish"),
                    ("gd", "Scottish Gaelic"),
                    ("gl", "Galician"),
                    ("he", "Hebrew"),
                    ("hi", "Hindi"),
                    ("hr", "Croatian"),
                    ("hsb", "Upper Sorbian"),
                    ("hu", "Hungarian"),
                    ("hy", "Armenian"),
                    ("ia", "Interlingua"),
                    ("id", "Indonesian"),
                    ("ig", "Igbo"),
                    ("io", "Ido"),
                    ("is", "Icelandic"),
                    ("it", "Italian"),
                    ("ja", "Japanese"),
                    ("ka", "Georgian"),
                    ("kab", "Kabyle"),
                    ("kk", "Kazakh"),
                    ("km", "Khmer"),
                    ("kn", "Kannada"),
                    ("ko", "Korean"),
                    ("ky", "Kyrgyz"),
                    ("lb", "Luxembourgish"),
                    ("lt", "Lithuanian"),
                    ("lv", "Latvian"),
                    ("mk", "Macedonian"),
                    ("ml", "Malayalam"),
                    ("mn", "Mongolian"),
                    ("mr", "Marathi"),
                    ("ms", "Malay"),
                    ("my", "Burmese"),
                    ("nb", "Norwegian Bokmål"),
                    ("ne", "Nepali"),
                    ("nl", "Dutch"),
                    ("nn", "Norwegian Nynorsk"),
                    ("os", "Ossetic"),
                    ("pa", "Punjabi"),
                    ("pl", "Polish"),
                    ("pt", "Portuguese"),
                    ("pt-br", "Brazilian Portuguese"),
                    ("ro", "Romanian"),
                    ("ru", "Russian"),
                    ("sk", "Slovak"),
                    ("sl", "Slovenian"),
                    ("sq", "Albanian"),
                    ("sr", "Serbian"),
                    ("sr-latn", "Serbian Latin"),
                    ("sv", "Swedish"),
                    ("sw", "Swahili"),
                    ("ta", "Tamil"),
                    ("te", "Telugu"),
                    ("tg", "Tajik"),
                    ("th", "Thai"),
                    ("tk", "Turkmen"),
                    ("tr", "Turkish"),
                    ("tt", "Tatar"),
                    ("udm", "Udmurt"),
                    ("uk", "Ukrainian"),
                    ("ur", "Urdu"),
                    ("uz", "Uzbek"),
                    ("vi", "Vietnamese"),
                    ("zh-hans", "Simplified Chinese"),
                    ("zh-hant", "Traditional Chinese"),
                ]
            ),
        ),
    ]
