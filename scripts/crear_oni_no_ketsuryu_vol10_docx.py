# -*- coding: utf-8 -*-
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from pathlib import Path
import shutil

doc = docx.Document()

# Margenes
for s in doc.sections:
    s.top_margin = Inches(1)
    s.bottom_margin = Inches(1)
    s.left_margin = Inches(1)
    s.right_margin = Inches(1)

# Titulo Principal
p_title = doc.add_paragraph()
p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
run_title = p_title.add_run("Oni no Ketsuryū (鬼の血流 - La Estirpe de la Sangre)\nVolumen 10: El Amanecer del Acero Santo (Gran Final de Saga)")
run_title.font.name = "Arial"
run_title.font.size = Pt(24)
run_title.font.bold = True
run_title.font.color.rgb = RGBColor(180, 0, 0)

# Subtitulo
p_sub = doc.add_paragraph()
p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
run_sub = p_sub.add_run("Obra Oficial por Nicolás Noguera\nEdición Digital Ilustrada - Conclusión de la Saga de 10 Volúmenes")
run_sub.font.name = "Arial"
run_sub.font.size = Pt(14)
run_sub.font.italic = True

doc.add_page_break()

base_dir = Path(r"C:\Proyectos\mis-libros-editorial\libros\oni-no-ketsuryu-volumen-10")
dest2 = Path(r"c:\Users\nicol\Downloads\MIS LIBROS\libros\oni-no-ketsuryu-volumen-10")

base_dir.mkdir(parents=True, exist_ok=True)
dest2.mkdir(parents=True, exist_ok=True)

# Asignar imagenes base si falta alguna
ref_dir = Path(r"C:\Proyectos\mis-libros-editorial\libros\oni-no-ketsuryu-volumen-9")
if not ref_dir.exists():
    ref_dir = Path(r"C:\Proyectos\mis-libros-editorial\libros\oni-no-ketsuryu-volumen-7")

all_imgs = [
    "portada.jpg", "thumbnail.jpg", "banner.jpg", "escena_1.jpg", "escena_climax.jpg",
    "escena_c1_e1.jpg", "escena_c1_e2.jpg", "escena_c1_e3.jpg",
    "escena_c2_e1.jpg", "escena_c2_e2.jpg", "escena_c2_e3.jpg",
    "escena_c3_e1.jpg", "escena_c3_e2.jpg", "escena_c3_e3.jpg",
    "escena_c4_e1.jpg", "escena_c4_e2.jpg", "escena_c4_e3.jpg",
    "escena_c5_e1.jpg", "escena_c5_e2.jpg", "escena_c5_e3.jpg"
]

for img_name in all_imgs:
    target1 = base_dir / img_name
    target2 = dest2 / img_name
    if not target1.exists():
        src = ref_dir / img_name
        if src.exists():
            shutil.copy(src, target1)
            shutil.copy(src, target2)

# Portada
portada_path = base_dir / "portada.jpg"
if portada_path.exists():
    doc.add_picture(str(portada_path), width=Inches(5.5))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_page_break()

# Texto del libro completo
capitulos = [
    {
        "titulo": "Capítulo 1: El Silencio del Alba",
        "escenas": [
            {
                "sub": "Escena 1: El Campo de Cenizas",
                "text": "La brisa de la mañana dispersó los últimos residuos de ceniza negra de Kageyama sobre las ruinas de la capital imperial. El sol de agosto se elevó radiante sobre el horizonte, bañando las piedras del cráter con una luz cálida y limpia.\n\nEl rugido de los combates, el chispazo de las espadas y el aire cargado de azufre cesaron por completo. Por primera vez en mil años, la atmósfera se sintió libre de cualquier rastro de energía demoníaca.\n\nEn medio de la plaza, Ren yacía inmóvil sobre el suelo agrietado. Su brazo derecho permanecía rígido junto a la empuñadura de la Katana del Sol, cuya hoja de tono rojo rubí comenzaba a enfriarse gradualmente, volviendo a su color oscuro original.\n\n—Ren... —susurró Miyuki, cayendo de rodillas al lado de su hermano.",
                "img": "escena_c1_e1.jpg"
            },
            {
                "sub": "Escena 2: El Pulso de la Sangre",
                "text": "Miyuki colocó sus manos sobre el pecho de Ren. La respiración del joven se había detenido por completo; las venas negras de la marca del sol se habían quedado heladas bajo su piel y no había pulso en su muñeca.\n\nSin dudarlo, Miyuki cerró los ojos y concentró la energía de su propia sangre, aquella que había conquistado la luz del sol. Pequeñas chispas de luz violeta y dorada brotaron de las palmas de sus manos, fluyendo directamente hacia el corazón de su hermano.\n\n—Prometimos volver juntos al hogar... —dijo Miyuki entre lágrimas, aumentando la presión de la curación—. ¡No me dejes sola ahora que la noche terminó!\n\nUn destello de luz recorrió el torso de Ren. Los médicos del gremio que corrían hacia la escena se detuvieron al presenciar la energía reconectando las células del joven.",
                "img": "escena_c1_e2.jpg"
            },
            {
                "sub": "Escena 3: El Despertar del Guerrero",
                "text": "Un latido seco y profundo resonó en el pecho de Ren: ¡BOOM!\n\nRen abrió los ojos de golpe, inhalando una bocanada de aire fresco de la mañana que llenó sus pulmones. La marca negra de su cara no desapareció por completo, pero se redujo a una cicatriz rosada sobre su mejilla derecha.\n\nMiyuki lo abrazó con fuerza, llorando sobre su hombro, mientras los cazadores sobrevivientes a su alrededor estallaban en vítores y lágrimas de alivio.\n\nRen miró sus propias manos y luego al cielo azul sin nubes.\n\n—Miyuki... la noche se acabó —dijo Ren con una sonrisa serena.",
                "img": "escena_c1_e3.jpg"
            }
        ]
    },
    {
        "titulo": "Capítulo 2: Las Lágrimas y la Paz",
        "escenas": [
            {
                "sub": "Escena 1: El Descanso de los Maestros Celestiales",
                "text": "En los días posteriores a la derrota del Rey Oni, la Sede Temporal del Gremio Cuervo se transformó en un refugio de sanación.\n\nGyomei (el Maestro Celestial de la Piedra) fue sepultado con honores en el templo de las glicinas, rodeado por las oraciones de todos los miembros del gremio. Kazuma y Giyuu, los Maestros Celestiales sobrevivientes, permanecieron en reposo recuperándose de sus heridas, sabiendo que su deber de mil años había sido finalmente completado.\n\nRen caminó por el jardín de flores de glicina llevando una bandeja con té caliente para los heridos.\n\n—Tu hermano Kenshin estaría orgulloso de ti, Ren —dijo Kazuma desde su pórtico, ajustándose el vendaje de su brazo.",
                "img": "escena_c2_e1.jpg"
            },
            {
                "sub": "Escena 2: La Despedida del Gremio",
                "text": "Tres semanas después de la batalla, se celebró la última asamblea general del Gremio Cuervo de Hermandad del Sol.\n\nEl joven heredero de la familia Ubuyashiki se presentó ante los sobrevivientes vistiendo un kimono blanco de ceremonia. Frente a él, sobre un altar de madera, descansaban las katanas de todos los cazadores que habían caído en combate.\n\n—Durante un siglo y diez generaciones, nuestra familia y el gremio han perseguido la sombra que azotaba a la humanidad —habló el joven líder con una reverencia profunda—. Hoy, la sombra ha desaparecido. Declaro la disolución oficial del Gremio Cuervo. Dejen sus espaldas y vivan vidas plenas como hombres y mujeres libres.\n\nLos cazadores se quitaron sus haoris de combate y los colocaron sobre el altar, llorando y sonriendo en un abrazo colectivo.",
                "img": "escena_c2_e2.jpg"
            },
            {
                "sub": "Escena 3: La Decisión de los Hermanos",
                "text": "Ren y Miyuki guardaron la Katana del Sol en una funda de madera tratada con aceite de glicina.\n\nKaito (su mentor) y el chico del haori amarillo los acompañaron hasta las puertas del santuario.\n\n—¿A dónde irán ahora? —preguntó Kaito, ajustando su máscara de Tengu a la cintura.\n\n—Volveremos a la montaña —respondió Ren, tomando la mano de Miyuki—. La herrería de nuestro padre nos espera. Es hora de encender el horno, pero esta vez no para hacer armas de guerra... sino para crear herramientas que ayuden a la gente a cultivar la tierra.\n\nLos amigos se despidieron con la promesa de reunirse cada año nuevo.",
                "img": "escena_c2_e3.jpg"
            }
        ]
    },
    {
        "titulo": "Capítulo 3: La Forja de la Nueva Era",
        "escenas": [
            {
                "sub": "Escena 1: El Regreso al Monte Kurodake",
                "text": "El viaje de regreso al monte Kurodake duró cuatro días. Al llegar a la cima, la nieve invernal de años atrás había dado paso a un prado verde lleno de flores silvestres que rodeaban el taller de la herrería.\n\nLa casa de madera de su infancia permanecía intacta. Ren y Miyuki abrieron las puertas de la vivienda, limpiaron el polvo del altar familiar y encendieron una vela en memoria de su padre y su madre.\n\nMiyuki, habiendo recuperado completamente su forma humana, preparó la primera comida casera en el taller después de tres años de viaje.\n\nEl olor a humo de madera y sopa de miso llenó nuevamente la herrería.",
                "img": "escena_c3_e1.jpg"
            },
            {
                "sub": "Escena 2: El Horno de la Tierra",
                "text": "Ren se colocó las ropas de trabajo de su padre y limpió los engranajes del taller.\n\nEncendió el fuego del horno con carbón de roble sagrado. Sin embargo, no vertió el mineral Tamahagane para moldear katanas: usó el acero para forjar cuchillos de cocina, arados de hierro para los agricultores del pueblo del valle y campanillas de viento que los pobladores colocaban en las puertas de sus casas.\n\nLa gente de las aldeas cercanas comenzó a visitar la herrería de los hermanos Hagane, agradecida por el trabajo artesanal del joven de la cicatriz.\n\nEl martilleo del taller de Ren ya no sonaba a desesperación o venganza; sonaba con el ritmo de la vida cotidiana.",
                "img": "escena_c3_e2.jpg"
            },
            {
                "sub": "Escena 3: Las Noches de Primavera",
                "text": "Pasaron dos años de paz absoluta.\n\nEn las noches de primavera, cuando los cerezos del monte Kurodake florecían, Kaito y el chico del haori amarillo visitaban la herrería. Se sentaban juntos en la veránda de madera a cenar bajo las estrellas, compartiendo historias y riendo sobre los recuerdos de sus viajes.\n\nLa Katana del Sol de Ren permanecía guardada en el altar de la casa como un monumento a la paz, sin necesidad de ser desenvainada nunca más.\n\nMiyuki contemplaba el cielo nocturno sin miedo a las sombras, disfrutando de la calidez de la brisa.",
                "img": "escena_c3_e3.jpg"
            }
        ]
    },
    {
        "titulo": "Capítulo 4: Las Memorias Grabadas",
        "escenas": [
            {
                "sub": "Escena 1: El Cuaderno de la Estirpe",
                "text": "Durante los años siguientes, Ren se dedicó a escribir e ilustrar a mano un registro completo de los acontecimientos vividos por el Gremio Cuervo.\n\nEn un cuaderno de papel arroz encuadernado en cuero, dibujó los rostros de Kenshin, Genba, Aoi, Kiri y todos los cazadores que habían sacrificado sus vidas durante la noche de los miles de años.\n\n—Para que las generaciones futuras no olviden que la paz no fue un regalo —dijo Ren a Miyuki—, sino el resultado del amor y la valentía de personas comunes.\n\nMiyuki colocó una flor de glicina seca entre las páginas del cuaderno antes de cerrarlo y guardarlo en el cofre del altar.",
                "img": "escena_c4_e1.jpg"
            },
            {
                "sub": "Escena 2: La Bendición de los Años",
                "text": "Los años transcurrieron con tranquilidad en el valle. Ren y Miyuki envejecieron rodeados por el respeto de su comunidad, dejando una descendencia que heredó el amor por la herrería y la vida sencilla de las montañas.\n\nLa leyenda de los Hermandad del Sol se disolvió gradualmente con el paso de las décadas, convirtiéndose en un cuento popular que los ancianos contaban a los niños junto al fuego durante las noches de invierno.\n\nPero el valor del acero y el significado de la Estilo de Dominio Solar quedaron grabados en la tierra misma.",
                "img": "escena_c4_e2.jpg"
            },
            {
                "sub": "Escena 3: El Puente del Tiempo",
                "text": "Cien años después.\n\nLas montañas del monte Kurodake y los campos de la capital imperial se habían transformado con el curso del siglo XX. Las chozas de madera y los senderos de piedra fueron reemplazados por rascacielos de cristal, avenidas iluminadas con luces de neón y trenes modernos que cruzaban la metrópolis de Tokio.\n\nSin embargo, el cielo de la ciudad era azul y despejado, libre de cualquier amenaza.\n\nEn las escuelas del nuevo siglo, los estudiantes vivían vidas tranquilas sin conocer el terror de las sombras nocturnas.",
                "img": "escena_c4_e3.jpg"
            }
        ]
    },
    {
        "titulo": "Capítulo 5: El Renacer bajo los Cerezos (Gran Final)",
        "escenas": [
            {
                "sub": "Escena 1: Los Estudiantes del Nuevo Siglo",
                "text": "En una mañana de primavera en el Tokio moderno, las hojas de los cerezos caían suavemente sobre el parque central.\n\nEntre la multitud de estudiantes caminaban dos jóvenes de quince años. El muchacho tenía el cabello negro despeinado y una leve marca de nacimiento rosa en su mejilla derecha; la chica llevaba una horquilla de mariposa en su cabello y sonreía mientras conversaban alegremente de camino a la escuela secundaria.\n\nEran las reencarnaciones de Ren y Miyuki, viviendo en un mundo lleno de paz, luz y oportunidades.\n\n—¡Llegaremos tarde a clase si no nos apuramos! —dijo la joven riendo mientras corría entre las flores.\n\n—¡Espérame! —respondió el chico, sonriendo con la misma mirada cálida del pasado.",
                "img": "escena_c5_e1.jpg"
            },
            {
                "sub": "Escena 2: El Museo del Acero",
                "text": "Al cruzar la calle del centro cultural de la ciudad, los estudiantes pasaron por la entrada del Museo Nacional de Historia.\n\nDentro de la galería principal, protegida en una vitrina de cristal iluminada, descansaba la antigua Katana del Sol que Ren había empuñado cuatrocientos años atrás. A su lado, abierto en la página final, se encontraba el Cuaderno de la Estirpe, conservado en perfecto estado.\n\nLos visitantes del museo leían la inscripción grabada en la placa de bronce del monumento:\n\n\"Dedicado a aquellos que caminaron por la noche para que nosotros pudiéramos caminar bajo el sol.\"",
                "img": "escena_c5_e2.jpg"
            },
            {
                "sub": "Escena 3: La Mirada hacia el Mañana (Cierre de la Saga)",
                "text": "El joven del uniforme escolar se detuvo un segundo frente a la cristalera del parque que reflejaba la vista del museo y los cerezos en flor.\n\nPor un instante, al tocar la marca rosa de su mejilla, un destello de calor reconfortante recorrió su pecho, recordándole la promesa de protección que había hecho siglos atrás.\n\nMiró a su hermana, quien le hacía señas con la mano desde la entrada de la escuela bajo la luz dorada del sol de la mañana.\n\nEl muchacho sonrió, dio un paso al frente y corrió hacia el futuro brillante que habían conquistado juntos.\n\n\n                  [ FIN DE ONI NO KETSURYŪ ]\n                  [ FIN DE LA SAGA DE 10 VOLÚMENES ]",
                "img": "escena_c5_e3.jpg"
            }
        ]
    }
]

for cap in capitulos:
    p_c = doc.add_paragraph()
    run_c = p_c.add_run(cap["titulo"])
    run_c.font.name = "Arial"
    run_c.font.size = Pt(18)
    run_c.font.bold = True
    run_c.font.color.rgb = RGBColor(160, 0, 0)
    
    for esc in cap["escenas"]:
        p_sub = doc.add_paragraph()
        run_sub = p_sub.add_run(esc["sub"])
        run_sub.font.name = "Arial"
        run_sub.font.size = Pt(14)
        run_sub.font.bold = True
        run_sub.font.color.rgb = RGBColor(50, 50, 50)
        
        p_t = doc.add_paragraph()
        run_t = p_t.add_run(esc["text"])
        run_t.font.name = "Calibri"
        run_t.font.size = Pt(12)
        
        img_path = base_dir / esc["img"]
        if img_path.exists():
            doc.add_picture(str(img_path), width=Inches(5.5))
            doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.add_paragraph()
        
    doc.add_page_break()

docx_out1 = base_dir / "libro.docx"
docx_out2 = dest2 / "libro.docx"

doc.save(str(docx_out1))
doc.save(str(docx_out2))
print(f"Generated libro.docx for Vol 10 successfully at {docx_out1}")
