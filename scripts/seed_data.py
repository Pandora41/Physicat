import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import Lesson, Quiz, Question

app = create_app()

with app.app_context():
    # Check kalau data udah ada
    if Lesson.query.first():
        print("Data already exists!")
    else:
        # Lesson 1: Gelombang
        lesson1 = Lesson(
            title="Gelombang",
            slug="gelombang",
            category="Gelombang",
            description="Pelajari konsep dasar gelombang: transversal, longitudinal, dan superposisi",
            content_html="""
                <h2>Apa itu Gelombang?</h2>
                <p>Gelombang adalah getaran yang merambat melalui medium atau ruang hampa.</p>
                
                <h3>Jenis-jenis Gelombang</h3>
                <ul>
                    <li><strong>Gelombang Transversal:</strong> Arah getaran tegak lurus arah rambat</li>
                    <li><strong>Gelombang Longitudinal:</strong> Arah getaran sejajar arah rambat</li>
                    <li><strong>Gelombang Stasioner:</strong> Hasil superposisi 2 gelombang berlawanan arah</li>
                </ul>
                
                <h3>Rumus Dasar</h3>
                <p>v = f × λ</p>
                <p>Dimana: v = kecepatan, f = frekuensi, λ = panjang gelombang</p>
            """,
            order_index=1
        )
        db.session.add(lesson1)
        db.session.flush()
        
        # Quiz 1
        quiz1 = Quiz(
            lesson_id=lesson1.id,
            title="Quiz Gelombang Dasar",
            description="Uji pemahamanmu tentang konsep dasar gelombang"
        )
        db.session.add(quiz1)
        db.session.flush()
        
        # Questions
        q1 = Question(
            quiz_id=quiz1.id,
            question_text="Apa yang dimaksud dengan gelombang transversal?",
            options=[
                "Gelombang yang arah getarannya sejajar dengan arah rambat",
                "Gelombang yang arah getarannya tegak lurus dengan arah rambat",
                "Gelombang yang tidak memerlukan medium",
                "Gelombang yang tidak memiliki frekuensi"
            ],
            correct_answer=1,
            explanation="Gelombang transversal memiliki arah getaran yang tegak lurus dengan arah rambatnya. Contoh: gelombang pada tali.",
            order_index=1
        )
        
        q2 = Question(
            quiz_id=quiz1.id,
            question_text="Rumus kecepatan gelombang adalah...",
            options=[
                "v = f + λ",
                "v = f - λ",
                "v = f × λ",
                "v = f / λ"
            ],
            correct_answer=2,
            explanation="Kecepatan gelombang = frekuensi × panjang gelombang (v = f × λ)",
            order_index=2
        )
        
        q3 = Question(
            quiz_id=quiz1.id,
            question_text="Gelombang suara di udara termasuk jenis gelombang...",
            options=[
                "Transversal",
                "Longitudinal",
                "Stasioner",
                "Elektromagnetik"
            ],
            correct_answer=1,
            explanation="Gelombang suara di udara adalah gelombang longitudinal karena arah getaran partikel udara sejajar dengan arah rambat gelombang.",
            order_index=3
        )
        
        db.session.add_all([q1, q2, q3])
        
        # Lesson 2: BB84 QKD
        lesson2 = Lesson(
            title="BB84 Quantum Key Distribution",
            slug="bb84",
            category="Quantum",
            description="Pelajari protokol kriptografi kuantum BB84",
            content_html="""
                <h2>Apa itu BB84?</h2>
                <p>BB84 adalah protokol distribusi kunci kuantum yang dikembangkan oleh Charles Bennett dan Gilles Brassard pada tahun 1984.</p>
                
                <h3>Prinsip Dasar</h3>
                <p>BB84 menggunakan prinsip mekanika kuantum untuk mendeteksi penyadapan. Jika ada pihak ketiga (Eve) yang mencoba menyadap, keadaan kuantum akan berubah dan bisa dideteksi.</p>
                
                <h3>Proses BB84</h3>
                <ol>
                    <li>Alice mengirim foton dengan basis acak</li>
                    <li>Bob mengukur dengan basis acak</li>
                    <li>Mereka membandingkan basis (bukan hasil)</li>
                    <li>Bit dengan basis yang sama menjadi kunci</li>
                    <li>Check QBER untuk deteksi penyadapan</li>
                </ol>
            """,
            order_index=2
        )
        db.session.add(lesson2)
        
        db.session.commit()
        print("Seed data created successfully!")
        print(f"- Lesson 1: {lesson1.title} (slug: {lesson1.slug})")
        print(f"- Lesson 2: {lesson2.title} (slug: {lesson2.slug})")
        print(f"- Quiz: {quiz1.title} with {len([q1, q2, q3])} questions")