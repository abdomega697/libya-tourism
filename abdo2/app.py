import os

from flask import Flask, render_template

app = Flask(__name__)

# بيانات المناطق السياحية في ليبيا
regions_data = [
    {
        'id': 1,
        'name': 'طرابلس',
        'name_en': 'Tripoli',
        'image': 'tripoli.jpg',
        'description': 'عاصمة ليبيا وأكبر مدنها، تجمع بين الأصالة والحداثة',
        'highlights': ['المدينة القديمة', 'قوس ماركوس أوريليوس', 'سراي الحمراء', 'ساحة الشهداء'],
        'best_time': 'مارس - مايو / سبتمبر - نوفمبر',
        'history': 'تأسست في القرن السابع قبل الميلاد على يد الفينيقيين'
    },
    {
        'id': 2,
        'name': 'بنغازي',
        'name_en': 'Benghazi',
        'image': 'benghazi.jpg',
        'description': 'ثاني أكبر مدن ليبيا، عروس البحر المتوسط',
        'highlights': ['الكيش', 'مبنى البلدية', 'شاطئ الصابري', 'كهوف قمينس'],
        'best_time': 'أبريل - أكتوبر',
        'history': 'تأسست تحت اسم يوسبريدس ثم برنيس'
    },
    {
        'id': 3,
        'name': 'لبدة الكبرى',
        'name_en': 'Leptis Magna',
        'image': 'leptis-magna.jpg',
        'description': 'أروع مدينة رومانية محفوظة في العالم',
        'highlights': ['المنتدى', 'قوس سيبتيموس سيفيروس', 'الحمامات', 'المسرح الروماني', 'السوق'],
        'best_time': 'أكتوبر - أبريل',
        'history': 'مسجلة ضمن قائمة اليونسكو للتراث العالمي'
    },
    {
        'id': 4,
        'name': 'غدامس',
        'name_en': 'Ghadames',
        'image': 'ghadames.jpg',
        'description': 'لؤلؤة الصحراء، المدينة البيضاء',
        'highlights': ['المدينة القديمة المسقوفة', 'أسواق غدامس', 'بيوت الطين'],
        'best_time': 'نوفمبر - فبراير',
        'history': 'أقدم مدينة محصنة في الصحراء، موقع تراث عالمي'
    },
    {
        'id': 5,
        'name': 'جبل أكاكوس',
        'name_en': 'Akakus Mountains',
        'image': 'akakus.jpg',
        'description': 'متحف فني مفتوح في قلب الصحراء',
        'highlights': ['الرسوم الصخرية', 'القوس الطبيعي', 'الكثبان الرملية', 'الوديان'],
        'best_time': 'ديسمبر - فبراير',
        'history': 'آثار بشرية تعود لأكثر من 12000 سنة'
    },
    {
        'id': 6,
        'name': 'صبراتة',
        'name_en': 'Sabratha',
        'image': 'sabratha.jpg',
        'description': 'مدينة رومانية ساحرة على البحر المتوسط',
        'highlights': ['المسرح الروماني', 'المعابد', 'الفيلات البحرية', 'المتحف'],
        'best_time': 'مارس - مايو / سبتمبر - نوفمبر',
        'history': 'تأسست في القرن السادس قبل الميلاد'
    },
    {
        'id': 7,
        'name': 'شحات (قورينا)',
        'name_en': 'Cyrene',
        'image': 'cyrene.jpg',
        'description': 'جوهرة الجبل الأخضر',
        'highlights': ['معبد زيوس', 'معبد أبولو', 'المقابر الملكية', 'الينابيع المقدسة'],
        'best_time': 'أبريل - أكتوبر',
        'history': 'أهم المدن الإغريقية في أفريقيا'
    },
    {
        'id': 8,
        'name': 'الجبل الغربي (جبل نفوسة)',
        'name_en': 'Jebel Nafusa',
        'image': 'jebel-nafusa.jpg',
        'description': 'منطقة جبلية خلابة تتميز بالمناظر الطبيعية الساحرة والهندسة المعمارية الفريدة',
        'highlights': ['قرى الجبل', 'المسار الجبلي', 'المناظر الطبيعية', 'بيوت الأمازيغ'],
        'best_time': 'مارس - مايو / سبتمبر - نوفمبر',
        'history': 'منطقة جبلية تمتد من شمال غرب ليبيا، تشتهر بقرى الأمازيغ التقليدية'
    },
    {
        'id': 9,
        'name': 'الصحراء الليبية',
        'name_en': 'Libyan Desert',
        'image': 'libyan-desert.jpg',
        'description': 'أجمل صحاري العالم، كثبان ذهبية تمتد لمسافات شاسعة',
        'highlights': ['كثبان مرزق الرملية', 'وادي الهي', 'الرسوم الصخرية', 'التخييم تحت النجوم'],
        'best_time': 'نوفمبر - فبراير',
        'history': 'جزء من الصحراء الكبرى، تحتوي على أقدم الرسوم الصخرية في العالم'
    },
    {
        'id': 10,
        'name': 'بحيرة قبرعون',
        'name_en': 'Gaberoun Lake',
        'image': 'gaberoun-lake.jpg',
        'description': 'بحيرة جميلة في قلب الصحراء الليبية، مياهها زرقاء صافية',
        'highlights': ['المياه الزرقاء', 'واحة النخيل', 'التخييم', 'تصوير غروب الشمس'],
        'best_time': 'أكتوبر - مارس',
        'history': 'بحيرة مالحة تقع في واحة في جنوب ليبيا، مقصد سياحي شهير'
    },
    {
        'id': 11,
        'name': 'سواحل ليبيا',
        'name_en': 'Libyan Coasts',
        'image': 'libyan-coasts.jpg',
        'description': 'أطول سواحل البحر المتوسط، تمتد لأكثر من 2000 كم بشواطئ رملية خلابة',
        'highlights': ['شاطئ درنة', 'شاطئ الخمس', 'شاطئ صبراتة', 'الرياضات المائية'],
        'best_time': 'مايو - أكتوبر',
        'history': 'ساحل ليبيا على البحر المتوسط يمتد من الحدود التونسية إلى الحدود المصرية'
    },
    {
        'id': 12,
        'name': 'درنة',
        'name_en': 'Derna',
        'image': 'derna.jpg',
        'description': 'جوهرة الساحل الشرقي، تتميز بشلالاتها الجميلة وشواطئها الساحرة وسط الجبال',
        'highlights': ['شلال درنة', 'وادي درنة', 'ساحة الشهداء', 'المسجد العتيق'],
        'best_time': 'مايو - أكتوبر',
        'history': 'مدينة تاريخية كانت جزءاً من الطريق التجاري القديم، تشتهر بطبيعتها الخلابة'
    },
]

# بيانات المطبخ الليبي
libyan_food = [
    {'name': 'البازين', 'description': 'الطبق الوطني الليبي، يقدم مع صلصة اللحم والبطاطس والبيض', 'ingredients': 'الشعير - اللحم - البطاطس - البيض - الطماطم'},
    {'name': 'الكسكس', 'description': 'طبق شعبي أصيل يقدم مع الخضار واللحم', 'ingredients': 'السميد - الخضار - اللحم - الحمص'},
    {'name': 'المبرومة', 'description': 'طبق لذيذ من المعكرونة المحشية باللحم', 'ingredients': 'المعكرونة - اللحم المفروم - البصل - البهارات'},
    {'name': 'العصيدة', 'description': 'حلى ليبي تقليدي يقدم في المناسبات', 'ingredients': 'الدقيق - العسل - السمن - التمر'},
    {'name': 'الرفيصة', 'description': 'طبق شعبي من الخبز المفتت بالمرق', 'ingredients': 'الخبز - اللحم - البصل - البهارات'},
    {'name': 'الشوربة الليبية', 'description': 'شوربة غنية بالخضار واللحم', 'ingredients': 'اللحم - الخضار - المعكرونة - البهارات'},
]

@app.route('/')
def index():
    return render_template('index.html', regions=regions_data)

@app.route('/regions')
def regions():
    return render_template('regions.html', regions=regions_data)

@app.route('/region/<int:region_id>')
def region_detail(region_id):
    region = next((r for r in regions_data if r['id'] == region_id), None)
    if region is None:
        return "المنطقة غير موجودة", 404
    return render_template('region_detail.html', region=region)

@app.route('/attractions')
def attractions():
    return render_template('attractions.html', regions=regions_data)

@app.route('/culture')
def culture():
    return render_template('culture.html', foods=libyan_food)

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
    if __name__ == '__main__':
        app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))