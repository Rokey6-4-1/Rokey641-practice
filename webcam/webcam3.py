import cv2



roi_hist = None 
win_name = 'MeanShift Tracking' 

termination = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)

x, y, w, h = 250, 120, 150, 200



cap = cv2.VideoCapture(0) 

if not cap.isOpened():
    print("오류: 비디오 파일을 열 수 없습니다. 파일을 업로드했는지 확인하세요.")
    exit()


ret, frame = cap.read()
if not ret:
    print("오류: 첫 프레임을 읽을 수 없습니다.")
    exit()


roi = frame[y:y + h, x:x + w]
roi_hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
roi_hist = cv2.calcHist([roi_hsv], [0], None, [180], [0, 180])

cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

print(f"초기 추적 대상 영역 설정 완료: (x={x}, y={y}, w={w}, h={h})")


while cap.isOpened() :
    ret, frame = cap.read()
    if not ret:
        break

    img_draw = frame.copy() 

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    dst = cv2.calcBackProject([hsv], [0], roi_hist, [0, 180], 1)

    ret, (x, y, w, h) = cv2.meanShift(dst, (x, y, w, h), termination)

    cv2.rectangle(img_draw, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow(win_name, img_draw)
    if cv2.waitKey(1) ==  ord('q'):
        break

cap.release()
cv2.destroyAllWindows()