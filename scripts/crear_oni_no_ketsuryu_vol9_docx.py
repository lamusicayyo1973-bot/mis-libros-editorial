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
run_title = p_title.add_run("Oni no Ketsuryū (鬼の血流 - La Estirpe de la Sangre)\nVolumen 9: La Noche de los Noventa Minutos")
run_title.font.name = "Arial"
run_title.font.size = Pt(24)
run_title.font.bold = True
run_title.font.color.rgb = RGBColor(180, 0, 0)

# Subtitulo
p_sub = doc.add_paragraph()
p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
run_sub = p_sub.add_run("Obra Oficial por Nicolás Noguera\nEdición Digital Ilustrada")
run_sub.font.name = "Arial"
run_sub.font.size = Pt(14)
run_sub.font.italic = True

doc.add_page_break()

base_dir = Path(r"C:\Proyectos\mis-libros-editorial\libros\oni-no-ketsuryu-volumen-9")
dest2 = Path(r"c:\Users\nicol\Downloads\MIS LIBROS\libros\oni-no-ketsuryu-volumen-9")

base_dir.mkdir(parents=True, exist_ok=True)
dest2.mkdir(parents=True, exist_ok=True)

# Asignar imagenes base si falta alguna
ref_dir = Path(r"C:\Proyectos\mis-libros-editorial\libros\oni-no-ketsuryu-volumen-8")

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
        "titulo": "Capítulo 1: La Emergencia a la Ciudad",
        "escenas": [
            {
                "sub": "Escena 1: La Ruptura de la Tierra",
                "text": "El suelo en el centro de la capital imperial crujió con una fuerza sísmica. Cientos de puertas de madera, plataformas de tatami y columnas del Castillo Infinito salieron disparadas hacia la superficie, destruyendo el pavimento y dejando un cráter de doscientos metros de ancho en la plaza principal de la ciudad.\n\nEntre las nubes de polvo y escombros, la luz de la luna llena iluminó los restos de la fortaleza colapsada.\n\nRen se reincorporó entre los cascotes, apoyándose en la Katana del Sol de hoja roja incandescente. A su lado, Miyuki, Sanemi y Gyomei emergieron del abismo, gravemente heridos pero con las marcas encendidas en su piel.\n\n—¡Salimos a la superficie! —gritó Sanemi, limpiándose la sangre del rostro—. ¿Dónde está Muzan?",
                "img": "escena_c1_e1.jpg"
            },
            {
                "sub": "Escena 2: La Transformación de la Bestia",
                "text": "Desde el centro del cráter, una explosión de carne y sangre destruyó las rocas circundantes.\n\nMuzan emergió en su forma de combate definitiva. Su cuerpo estaba cubierto por docenas de bocas con dientes afilados que emitían un siseo macabro; de sus muslos y espalda brotaban ocho látigos de carne y hueso equipados con sierras afiladas que se movían a una velocidad imperceptible para el ojo humano.\n\n—Han destruido mi dominio... han matado a mis Lunares... —resonó la voz de Muzan con una furia helada que congeló el aire—. Pero miren al cielo: faltan noventa minutos para el amanecer. Ninguno de ustedes vivirá para ver la luz del sol.\n\nMuzan agitó sus látigos, reduciendo a polvo tres edificios de piedra en una fracción de segundo.",
                "img": "escena_c1_e2.jpg"
            },
            {
                "sub": "Escena 3: La Primera Envestida",
                "text": "Gyomei (el Pilar de la Piedra) fue el primero en saltar, lanzando su hacha y bola de picos contra el torso de Muzan. Sin embargo, la velocidad de reacción del Rey Oni superaba todo lo visto hasta ahora.\n\nUn solo latigazo de carne cortó la cadena de Gyomei y le infligió un corte profundo en la pierna izquierda, inyectando la propia sangre venenosa de Muzan en su sistema vascular.\n\nSanemi y Giyuu atacaron por los flancos, pero sus katanas fueron desviadas por la masa de tentáculos antes de tocar la piel del enemigo.\n\n—¡Es demasiado rápido! —advirtió Giyuu—. ¡Ni siquiera con el Mundo Transparente podemos predecir la trayectoria de los ocho látigos al mismo tiempo!\n\nRen apretó los dientes. Las venas de su cuello comenzaron a volverse negras por el veneno de la primera ráfaga.",
                "img": "escena_c1_e3.jpg"
            }
        ]
    },
    {
        "titulo": "Capítulo 2: El Veneno en la Sangre",
        "escenas": [
            {
                "sub": "Escena 1: El Límite Humano",
                "text": "A los quince minutos del combate en la superficie, la mitad de las fuerzas del Gremio Cuervo habían sido derribadas. El veneno de Muzan destruía las células de los cazadores de forma acelerada, provocando parálisis muscular y vómitos de sangre en los luchadores.\n\nRen cayó sobre una rodilla en el pavimento agrietado, sintiendo que su vista se apagaba lentamente.\n\n—Es inútil... la fisiología humana no puede metabolizar la sangre pura de mi cuerpo —se burló Muzan, avanzando con paso firme hacia Ren—. Han perdido.\n\nDe pronto, un pequeño gato blanco con pergaminos mágicos en su lomo saltó desde las sombras del cráter, disparando tres jeringas de vidrio directo al cuello de Ren, Gyomei y Sanemi.",
                "img": "escena_c2_e1.jpg"
            },
            {
                "sub": "Escena 2: La Herencia de Tamayo",
                "text": "Las jeringas contenían el suero purificador desarrollado por Tamayo antes de su muerte.\n\nEl veneno en la sangre de Ren fue neutralizado de golpe, permitiéndole respirar nuevamente. Al mismo tiempo, dentro del cuerpo de Muzan, un dolor agudo paralizó sus extremidades por un milisegundo.\n\nMuzan sintió que su masa muscular se volvía más pesada y su tasa de regeneración disminuía a la mitad.\n\nEn su mente resonó el recuerdo de la voz de Tamayo:\n\n«Muzan... la droga que introduje en tu cuerpo contiene cuatro sustancias combinadas: conversión humana, envejecimiento acelerado de cincuenta años por minuto, prevención de división celular y destrucción de tejidos.»\n\n—¡Cincuenta años por minuto...! —comprendió Muzan con horror—. ¡He envejecido más de nueve mil años desde que comenzó la batalla!",
                "img": "escena_c2_e2.jpg"
            },
            {
                "sub": "Escena 3: El Sacrificio de las Tropas",
                "text": "Sabiendo que Muzan estaba debilitado, los cazadores de rango inferior del Gremio Cuervo —jóvenes que no poseían respiraciones especiales ni marcas— tomaron una decisión heroica.\n\nSe lanzaron en masa frente a los látigos de Muzan, usando sus propios cuerpos, carruajes de madera y escudos de metal para amortiguar los golpes y proteger a los Pilares heridos.\n\n—¡Protejan al chico de la marca del sol! —gritaban los soldados mientras caían—. ¡Él es nuestra única esperanza para llegar al amanecer!\n\nRen miró el sacrificio de sus compañeros con lágrimas de sangre rodando por sus mejillas.\n\n—No dejaré... que la muerte de ninguno de ustedes sea en vano —susurró Ren, poniéndose de pie con la katana roja ardiendo en su mano.",
                "img": "escena_c2_e3.jpg"
            }
        ]
    },
    {
        "titulo": "Capítulo 3: La Secuencia del Sol",
        "escenas": [
            {
                "sub": "Escena 1: El Descubrimiento del Bucle",
                "text": "Ren cerró los ojos en medio del caos del campo de batalla. En su mente, las páginas de Los Diarios del Sol se desplegaron con una claridad cristalina.\n\nComprendió finalmente la intención del primer usuario de la respiración:\nLas doce formas de la Danza del Sol no eran técnicas individuales para ser usadas al azar. Eran los eslabones de una sola cadena. Al ejecutar la primera postura y conectarla sin interrupción con la duodécima en un bucle infinito, los doce movimientos formaban la Decimotercera Postura, diseñada para destruir los doce órganos vitales (siete corazones y cinco cerebros) que Muzan movía constantemente dentro de su cuerpo.\n\nRen ajustó la postura de sus pies sobre las losas de piedra.\n\n—Danza del Sol... Primera Postura: Vals del Fuego.",
                "img": "escena_c3_e1.jpg"
            },
            {
                "sub": "Escena 2: La Rueda de Fuego",
                "text": "Ren se convirtió en un fénix incandescente.\n\nVals.\nCielo Azul.\nEspejo del Sol Feroz.\nArco del Sol Poniente.\nLanza del Sol.\n\nSu katana de tono rojo rubí se movía en un bucle continuo de llamas doradas que cortaba los tentáculos de Muzan a medida que intentaban regenerarse. La temperatura corporal de Ren subió a más de cuarenta grados, haciendo que la marca de su cara brillara con un calor blanco incandescente.\n\nMiyuki saltó a su lado, usando sus llamas púrpuras para congelar la regeneración de las heridas que Ren abría en el torso del Rey Oni.\n\n—¡Este muchacho... está ejecutando la misma danza de ese hombre de la era Sengoku! —pensó Muzan con pánico absoluto.",
                "img": "escena_c3_e2.jpg"
            },
            {
                "sub": "Escena 3: La Desesperación del Rey",
                "text": "A los cuarenta y cinco minutos de la cuenta regresiva, Muzan intentó dividirse en mil ochocientos fragmentos de carne para escapar por las alcantarillas de la ciudad, tal como lo había hecho cuatrocientos años atrás.\n\nSin embargo, la droga de Tamayo impidió la división celular.\n\nAl ver que no podía dividirse ni regenerarse a tiempo, Muzan liberó una onda de choque sónica desde su torso que arrojó a Ren, Sanemi y Giyuu contra los muros de la plaza, dejándolos inconscientes por varios minutos.\n\nMuzan, con el cuerpo deformado y sangrando por las heridas antiguas que la katana de Ren había reabierto, comenzó a arrastrarse hacia el callejón más oscuro de la ciudad para huir del sol naciente.",
                "img": "escena_c3_e3.jpg"
            }
        ]
    },
    {
        "titulo": "Capítulo 4: La Luz en el Horizonte",
        "escenas": [
            {
                "sub": "Escena 1: El Cambio en el Cielo",
                "text": "Faltaban exactamente quince minutos para el amanecer.\n\nEl cielo nocturno sobre la capital imperial comenzó a cambiar de tono, pasando del negro azabache a un azul marino profundo en el horizonte oriental. Las estrellas comenzaron a apagarse una por una.\n\nMuzan sintió el cambio de temperatura en el aire y entró en un estado de histeria ciega.\n\nSu cuerpo comenzó a expandirse de forma grotesca, creando una masa de carne gigante de diez metros de altura con forma de bebé deforme. Esta armadura orgánica le permitía proteger su verdadero cuerpo de los rayos solares y excavar en la tierra para enterrarse.\n\n—¡No dejen que se entierre! —gritó el Pilar del Viento, reincorporándose con el brazo izquierdo roto.",
                "img": "escena_c4_e1.jpg"
            },
            {
                "sub": "Escena 2: Los Obstáculos de la Ciudad",
                "text": "Los cazadores sobrevivientes usaron todo lo que tenían a mano para bloquear el avance del monstruo de carne.\n\nCarruajes de madera, vigas de hierro de los edificios destruidos e incluso un autobús de vapor de la era Meiji fueron empujados por los soldados para aplastar la cabeza del gigante de carne y mantenerlo expuesto bajo el cielo abierto.\n\nGiyuu y Sanemi atacaron las extremidades inferiores del gigante con sus katanas rojas, evitando que la criatura pudiera avanzar hacia las sombras de las callejuelas.\n\n—¡Resistan! —gritaba Sanemi entre dientes—. ¡El sol ya está saliendo!",
                "img": "escena_c4_e2.jpg"
            },
            {
                "sub": "Escena 3: El Regreso del Cazador",
                "text": "Desde lo alto de un carruaje destruido, Ren emergió nuevamente.\n\nHabía perdido la visión de su ojo derecho y la mitad de su haori negro estaba quemado, pero la Katana del Sol en sus manos emitía un brillo rojo tan intenso que parecía fundirse con el aire.\n\nInhaló aire hasta el fondo de sus alvéolos, activando la Decimotercera Postura por última vez.\n\n—Danza del Sol... Decimotercera Postura Definitiva.\n\nRen se lanzó como un meteoro de luz dorada directo al corazón del gigante de carne.",
                "img": "escena_c4_e3.jpg"
            }
        ]
    },
    {
        "titulo": "Capítulo 5: La Estocada del Sol (Clímax del Volumen 9)",
        "escenas": [
            {
                "sub": "Escena 1: El Empalamiento del Rey",
                "text": "Ren clavó la Katana del Sol directamente en el centro del pecho de la masa de carne de Muzan, atravesando el núcleo donde el verdadero cuerpo del Rey Oni se escondía.\n\nLa fuerza del impacto fijó al monstruo gigante contra el muro de piedra de la plaza principal, impidiéndole dar un solo paso más.\n\nMiyuki corrió al lado de su hermano y colocó sus manos sobre la empuñadura de la espada, mezclando su sangre demoníaca de llamas púrpuras con el fuego dorado de Ren.\n\n—¡No te moverás de aquí! —gritaron los dos hermanos al unísono.\n\nMuzan envolvió sus tentáculos alrededor del cuerpo de Ren, intentando aplastarle las costillas para liberarse, pero Ren no soltó la empuñadura de su espada.",
                "img": "escena_c5_e1.jpg"
            },
            {
                "sub": "Escena 2: El Primer Rayo de Sol",
                "text": "El borde superior del sol matutino emergió finalmente sobre los picos de las montañas del este.\n\nUn pilar de luz dorada y pura atravesó las nubes de la mañana y cayó directamente sobre la plaza central de la capital imperial, bañando el cuerpo de la masa de carne de Muzan por completo.\n\nUn silencio sepulcral dominó la ciudad durante una fracción de segundo.\n\nLuego, un alarido de agonía que no pertenecía a este mundo retumbó en el aire.",
                "img": "escena_c5_e2.jpg"
            },
            {
                "sub": "Escena 3: La Desintegración Absoluta (Cierre del Tomo 9)",
                "text": "Bajo la luz directa del sol, la masa de carne gigante de Muzan comenzó a disolverse a una velocidad irreversible. Sus tentáculos se convirtieron en cenizas de fuego rojo, sus bocas se cerraron para siempre y el verdadero cuerpo del Rey Oni comenzó a quemarse desde el interior.\n\nMuzan intentó transferir la totalidad de su sangre y sus recuerdos hacia el cuerpo de Ren en un último acto de desesperación espiritual.\n\nPero las llamas púrpuras de Miyuki y la voluntad inquebrantable de Ren rechazaron la conciencia de la criatura.\n\nEl cuerpo de Muzan se redujo a un puñado de cenizas negras que el viento de la mañana dispersó sobre las ruinas de la ciudad.\n\nEl Rey Oni, la pesadilla de mil años de la humanidad, había sido erradicado del planeta para siempre.\n\n\n                  [ CONTINUARÁ EN EL VOLUMEN 10 ]\n                  [ VOLUMEN FINAL: EL AMANECER DEL ACERO SANTO ]",
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
print(f"Generated libro.docx for Vol 9 successfully at {docx_out1}")
