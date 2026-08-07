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
run_title = p_title.add_run("Oni no Ketsuryū (鬼の血流 - La Estirpe de la Sangre)\nVolumen 7: El Asedio al Castillo Infinito")
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

base_dir = Path(r"C:\Proyectos\mis-libros-editorial\libros\oni-no-ketsuryu-volumen-7")
dest2 = Path(r"c:\Users\nicol\Downloads\MIS LIBROS\libros\oni-no-ketsuryu-volumen-7")

base_dir.mkdir(parents=True, exist_ok=True)
dest2.mkdir(parents=True, exist_ok=True)

# Asignar imagenes base si falta alguna
ref_dir = Path(r"C:\Proyectos\mis-libros-editorial\libros\oni-no-ketsuryu-volumen-6")

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
        "titulo": "Capítulo 1: El Laberinto Flotante",
        "escenas": [
            {
                "sub": "Escena 1: La Separación en el Abismo",
                "text": "La caída a través del espacio distorsionado del Castillo Infinito pareció durar una eternidad. Las estructuras de madera, salas de tatami invertidas y escaleras que desafiaban la gravedad giraban alrededor de los cazadores mientras la música del biwa resonaba en la penumbra.\n\nAl tocar tierra sobre el techo de una sala flotante, Ren se reincorporó de golpe con la katana del sol en la mano.\n\nA su lado sólo se encontraba el chico del haori amarillo. Los demás Pilares y los cientos de soldados del gremio habían sido dispersados por el poder del espacio demoníaco hacia diferentes sectores del castillo para ser emboscados individualmente.\n\n—Nos han separado a propósito... —dijo Ren, mirando hacia la caja de madera en su espalda donde Miyuki permanecía a salvo—. Quieren desgastarnos antes de que alcancemos a Muzan.",
                "img": "escena_c1_e1.jpg"
            },
            {
                "sub": "Escena 2: La Horda de los Pasillos",
                "text": "Antes de que pudieran planear una ruta, docenas de puertas de papel fusuma alrededor de la sala se abrieron al mismo tiempo.\n\nDe las sombras emergieron cientos de demonios menores creados por la carne de Muzan: criaturas deformes con múltiples ojos y garras de hierro que se lanzaron en masa desde el techo y las paredes.\n\nRen e Inosuke (el chico del haori amarillo en su estado de trance de trueno) se colocaron espalda con espalda.\n\n—Respiración de Sangre... Primera Postura: Tajo del Horno Olvidado.\n\nLa katana negra y roja de Ren trazó un arco de fuego dorado que redujo a cenizas a los diez primeros demonios de la vanguardia, mientras ráfagas de luz amarilla cortaban las paredes de madera a su alrededor.",
                "img": "escena_c1_e2.jpg"
            },
            {
                "sub": "Escena 3: La Guardiana del Biwa",
                "text": "A tres niveles de distancia sobre una plataforma suspendida, Nakime —la demonio ciega que controlaba el castillo con su biwa— tocaba las cuerdas con ritmo veloz. Cada nota alteraba la arquitectura de la fortaleza, separando a los cazadores que intentaban reunirse.\n\nEl Pilar de la Serpiente y la Pilar del Amor avanzaban hacia ella destruyendo los tabiques de madera.\n\n—Si no matamos a la mujer del biwa —gritó la Pilar del Amor ejecutando acrobacias con su espada flexible—, jamás llegaremos al centro donde se oculta Muzan.\n\nDesde las sombras detrás de Nakime, una figura de hielo cristalino descendió silenciosamente con dos abanicos en las manos.",
                "img": "escena_c1_e3.jpg"
            }
        ]
    },
    {
        "titulo": "Capítulo 2: La Venganza de las Flores",
        "escenas": [
            {
                "sub": "Escena 1: El Salón del Culto Helado",
                "text": "Kanae, la chica de la máscara de zorro y la túnica de mariposa, aterrizó en un salón amplio decorado con loto acuáticos y espejos de bronce.\n\nEn el centro del salón, sobre una pila de ropa de lujo, Doma —el Segundo Lunar Rojo— comía alegremente la energía de las personas que habían sido atraídas a su culto.\n\n—Vaya... una pequeña mariposa ha caído en mi red —dijo Doma, desplegando sus abanicos de cristal con sus ojos multicolores brillando de alegría falsa—. Hacía tiempo que no veía a alguien que usara veneno de glicina.\n\nKanae apretó la empuñadura de sus dagas. Reconoció el patrón del abanico: era el mismo demonio que años atrás había asesinado a su maestra.",
                "img": "escena_c2_e1.jpg"
            },
            {
                "sub": "Escena 2: La Niebla Helada contra la Picadura",
                "text": "Kanae se desplazó con una velocidad impresionante, utilizando la Respiración de la Picadura para trazar ráfagas de cortes rápidos que apuntaban directamente a los puntos vitales de Doma.\n\n—Respiración de la Picadura... Danza de la Mariposa: Capricho del Veneno.\n\nDoma desvió las dagas con sus abanicos de cristal, lanzando ráfagas de viento congelado que disminuyeron la temperatura de la sala a niveles bajo cero. El veneno de glicina impregnado en las hojas de Kanae entró en la piel de Doma, pero el demonio descompuso la toxina dentro de su estómago en cuestión de segundos.\n\n—Una toxina muy pura, pequeña mariposa —sonrió Doma—, pero mi cuerpo puede procesar cualquier veneno en poco tiempo.\n\nKanae cayó de rodillas sobre el suelo helado, sintiendo que sus bronquios se congelaban por la escarcha del aire.",
                "img": "escena_c2_e2.jpg"
            },
            {
                "sub": "Escena 3: El Sacrificio de la Toxina Concentrada",
                "text": "Sabiendo que no podría cortar la cabeza del Segundo Lunar usando la fuerza física, Kanae recordó la decisión que había tomado meses antes con la médica del gremio.\n\nDurante un año completo, Kanae había ingerido diariamente dosis controladas de veneno de glicina concentrado, convirtiendo su propio cuerpo, su sangre y sus órganos en una bomba química mortal para cualquier demonio que la devorara.\n\n—No necesito cortar tu cabeza para destruirte... —susurró Kanae con una sonrisa tranquila.\n\nDoma la atrapó con sus garras heladas y absorbió el cuerpo de Kanae dentro de su propia masa corporal.\n\nEn ese preciso segundo, las puertas del salón fueron reducidas a astillas por el salto de Ren y el chico del haori amarillo.",
                "img": "escena_c2_e3.jpg"
            }
        ]
    },
    {
        "titulo": "Capítulo 3: El Hielo Descompuesto",
        "escenas": [
            {
                "sub": "Escena 1: La Furia del Sol y el Trueno",
                "text": "—¡KANAE! —gritó Ren con una rabia ciega.\n\nLas venas de su rostro y su cuello se encendieron en un tono carmesí brillante. Ren inhaló todo el aire disponible y ejecutó tres movimientos consecutivos de la Danza del Sol, convirtiendo la sala congelada en un infierno de llamas doradas.\n\nEl chico del haori amarillo, al ver a su compañera caer, desató el Estilo del Trueno Inverso: Séptima Postura: Dios del Trueno, moviéndose tan rápido que la barrera de hielo de Doma fue destruida antes de que el demonio pudiera reaccionar.\n\nDoma intentó regenerar sus brazos para lanzar su técnica final, pero de pronto su cuerpo comenzó a derretirse desde el interior.",
                "img": "escena_c3_e1.jpg"
            },
            {
                "sub": "Escena 2: El Veneno de Setenta Kilos",
                "text": "El veneno de glicina concentrado en la sangre de Kanae —equivalente a setenta veces la dosis mortal— comenzó a liquefacer los órganos y la estructura ósea de Doma.\n\n—Imposible... ella... tenía el cuerpo lleno de veneno... —gimió Doma mientras sus piernas y su rostro se desintegraban en una masa informe.\n\nMiyuki saltó de la caja de madera y bañó la masa en descomposición de Doma con sus llamas púrpuras.\n\nRen no le dio tiempo a recuperarse: levantó la Katana del Sol y cortó lo que quedaba del cuello del Segundo Lunar Rojo con un tajo descendente de fuego dorado.\n\nLa cabeza de Doma cayó sobre la nieve artificial, disolviéndose en cenizas definitivas.",
                "img": "escena_c3_e2.jpg"
            },
            {
                "sub": "Escena 3: El Espíritu de la Mariposa",
                "text": "De entre las cenizas que se dispersaban en el aire, la ilusión del espíritu de Kanae emergió por un instante, luciendo sus alas de mariposa de luz.\n\nSonrió hacia Ren y Miyuki, dándoles la bendición final antes de desvanecerse hacia el firmamento.\n\nRen apretó los dientes, limpiándose las lágrimas de la cara, y recogió la horquilla de mariposa que Kanae había dejado sobre el suelo para colocársela a Miyuki en el cabello.\n\n—Faltan los dos últimos Lunares... —dijo Ren con voz firme—. Seguimos adelante.",
                "img": "escena_c3_e3.jpg"
            }
        ]
    },
    {
        "titulo": "Capítulo 4: La Sala de las Seis Lunas",
        "escenas": [
            {
                "sub": "Escena 1: El Gran Salón de los Espejos",
                "text": "Avanzando hacia el sector más profundo del castillo, Ren y el Pilar de la Niebla (Muichiro) llegaron al Salón de la Luna Llena, un espacio colosal donde no había paredes, sino miles de espadas rotas clavadas en la piedra.\n\nEn el centro del lugar, esperando con su kimono púrpura y sus seis ojos abiertos, se encontraba Kokushibo, el Primer Lunar Rojo.\n\nJunto a él, atada a una columna de piedra con cadenas de sangre, se encontraba la demonio del biwa (Nakime), cuyo control del castillo estaba siendo forzado por la propia voluntad de Kokushibo.\n\n—Han llegado lejos... —dijo Kokushibo, desenvainando la katana de carne cubierta de pupilas—. Pero aquí es donde la estirpe de los cazadores termina.",
                "img": "escena_c4_e1.jpg"
            },
            {
                "sub": "Escena 2: La Cacería de los Dos Pilares",
                "text": "Gyomei (el Pilar de la Piedra) y Sanemi (el Pilar del Viento, un hombre lleno de cicatrices que usaba técnicas de ráfagas cortantes) irrumpieron desde el techo, uniéndose a Muichiro y a Ren.\n\nCuatro de los guerreros más poderosos del gremio atacaron al Primer Lunar al mismo tiempo.\n\n—Respiración de la Piedra: Quinta Postura: Rueda de Piedra.\n—Respiración del Viento: Primera Postura: Torbellino Cortante.\n\nLa combinación de la bola de picos de Gyomei y las ráfagas de viento de Sanemi destruyeron la plataforma central. Pero Kokushibo ni siquiera cambió de postura: su Respiración de la Luna generó una tormenta de cientos de cuchillas de luz plateada que destrozaron la armadura y el cuerpo de los atacantes en un segundo.",
                "img": "escena_c4_e2.jpg"
            },
            {
                "sub": "Escena 3: El Sacrificio de la Niebla",
                "text": "Muichiro, el joven Pilar de la Niebla de catorce años, usó el Mundo Transparente para saltar directamente sobre la guardia de Kokushibo.\n\nAceptando que moriría en el intento, Muichiro dejó que la katana de seis ojos le atravesara el pecho, usándolo como freno para clavar su propia espada roja en el costado de Kokushibo, inmovilizando al demonio supremo por un segundo clave.\n\n—¡AHORA! ¡CORTEN SU CUELLO! —gritó Muichiro con sangre brotándole de la boca.\n\nGyomei y Sanemi descargaron todo el peso de sus armas sobre el cuello del Primer Lunar.",
                "img": "escena_c4_e3.jpg"
            }
        ]
    },
    {
        "titulo": "Capítulo 5: La Caída del Primer Samurai (Clímax del Volumen 7)",
        "escenas": [
            {
                "sub": "Escena 1: La Espada Roja de la Marca",
                "text": "Ren saltó por encima de la columna de espadas rotas.\n\nLa marca de la Danza del Sol en su cara brilló con un calor blanco incandescente. Al sostener la empuñadura de su katana con ambas manos, la Respiración de Sangre y la energía de la Danza del Sol hicieron que la hoja negra se volviera de un color rojo brillante que quemaba la regeneración de Kokushibo a nivel celular.\n\n—Danza del Sol... Decimoprimera Postura: Halo del Sol Abrillantado.\n\nRen ejecutó un corte giratorio que se unió al impacto del hacha de Gyomei.\n\nLa cabeza de Kokushibo, con sus seis ojos abiertos de impresión, fue finalmente amputada del cuerpo.",
                "img": "escena_c5_e1.jpg"
            },
            {
                "sub": "Escena 2: La Monstruosidad de la Regeneración",
                "text": "Pero la batalla no había terminado.\n\nLa cabeza decapitada de Kokushibo cayó al suelo, pero su cuerpo no se disolvió. Guiado por su deseo milenario de superar a su hermano y su rechazo a la derrota, el cuerpo del Primer Lunar comenzó a regenerar una nueva cabeza fea y monstruosa con cuernos y colmillos.\n\nSe estaba convirtiendo en un ser inmune a la decapitación por katanas.\n\nSin embargo, al mirarse en el reflejo de la hoja brillante de la espada de Ren, Kokushibo vio su nuevo rostro de monstruo deforme.\n\n—¿Es esto... en lo que me he convertido para ser el más fuerte? —pensó Kokushibo con un horror profundo en su alma—. ¿Un monstruo grotesco que olvidó el honor de los samuráis?",
                "img": "escena_c5_e2.jpg"
            },
            {
                "sub": "Escena 3: El Colapso de la Dimensión (Cierre del Tomo 7)",
                "text": "La duda en el corazón de Kokushibo provocó que la regeneración de su cuerpo se detuviera. El lugar donde la espada roja de Muichiro estaba clavada comenzó a disolver las venas del demonio desde adentro.\n\n—Hermano... lo siento... —susurró la voz original de Kokushibo mientras su cuerpo se convertía en cenizas negras y su flauta de la infancia caía sobre la piedra.\n\nAl morir el Primer Lunar, el control del castillo colapsó.\n\nYushiro (un aliado del gremio) tomó el control del cerebro de Nakime (la demonio del biwa), forzando a todo el Castillo Infinito a emerger hacia la superficie a una velocidad destructiva.\n\nLas estructuras de madera se hicieron pedazos cuando la fortaleza completa emergió a la superficie en el centro de la capital imperial, a solo una hora y media del amanecer.\n\nMuzan emergió de los escombros del palacio en su forma definitiva.\n\n\n                  [ CONTINUARÁ EN EL VOLUMEN 8 ]\n                  [ INICIO DE LA BATALLA DEL AMANECER ]",
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
print(f"Generated libro.docx for Vol 7 successfully at {docx_out1}")
