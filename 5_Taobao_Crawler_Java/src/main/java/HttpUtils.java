/*
@author:xinxintang
@create: 2018-06-22-2:07 PM
*/
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

import javax.swing.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class HttpUtils {
    private static String get(String url) {
        try {
            URL getUrl = new URL(url);
            HttpURLConnection connection = (HttpURLConnection) getUrl
                    .openConnection();
            connection.setRequestMethod("GET");
            connection.setRequestProperty("Accept", "*/*");
            connection
                    .setRequestProperty("User-Agent",
                            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; CIBA)");
            connection.setRequestProperty("Accept-Language", "zh-cn");
            connection.connect();
            BufferedReader reader = new BufferedReader(new InputStreamReader(connection.getInputStream(), "utf-8"));
            String line;
            StringBuffer result = new StringBuffer();
            while ((line = reader.readLine()) != null) {
                result.append(line);
            }
            reader.close();
            return result.toString();
        } catch (Exception e) {
            e.printStackTrace();
        }
        return null;
    }

    private static List<String> getImageSrc(String html) {
        // 获取img标签正则
        String IMGURL_REG = "<img.*src=(.*?)[^>]*?>";
        // 获取src路径的正则
        String IMGSRC_REG = "http:\"?(.*?)(\"|>|\\s+)";
        Matcher matcher = Pattern.compile(IMGURL_REG).matcher(html);
        List<String> listImgUrl = new ArrayList<String>();
        while (matcher.find()) {
            Matcher m = Pattern.compile(IMGSRC_REG).matcher(matcher.group());
            while (m.find()) {
                listImgUrl.add(m.group().substring(0, m.group().length() - 1));
            }
        }
        return listImgUrl;
    }

    public static void main(String[] args) {
        // Java Frame
        JFrame frame = new JFrame();
        frame.setResizable(false);
        frame.setSize(425, 400);
        frame.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
        frame.setLayout(null);
        frame.setLocationRelativeTo(null);
        final JTextField jTextField = new JTextField();
        jTextField.setBounds(100, 44, 200, 30);
        frame.add(jTextField);
        JButton jButton = new JButton("提取");
        jButton.setBounds(140, 144, 100, 30);
        frame.add(jButton);
        frame.setVisible(true);
        jButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                String url = jTextField.getText();
                if (url == null || url.equals("")) {
                    JOptionPane.showMessageDialog(null, "请填写抓取地址");
                    // https://www.toutiao.com/a6568327638044115460/
                    return;
                }
                String html = HttpUtils.get(url);
                assert html != null;
                Document doc = Jsoup.parse(html);
                Elements imgs = doc.getElementsByTag("img");
                for (Element img : imgs) {
                    String imgSrc = img.attr("src");
                    if (imgSrc.startsWith("//")) {
                        imgSrc = "http:" + imgSrc;
                    }
                    try {
                        Files.copy(new URL(imgSrc).openStream(), Paths.get("./img/" + UUID.randomUUID() + ".png"));
                    } catch (IOException e1) {
                        e1.printStackTrace();
                    }
                }
                JOptionPane.showMessageDialog(null, "抓取完成");
            }
        });
    }
}